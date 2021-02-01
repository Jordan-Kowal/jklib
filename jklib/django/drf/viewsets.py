"""
Viewset and mixin classes for DRF
Split into sub-categories:
    Mixins: Provide utility functions for viewsets (but do not inherit from them)
    Viewsets: Improved DRF ViewSets through custom mixins and utility functions
"""

# Django
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import mixins
from rest_framework.decorators import MethodMapper, action
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.viewsets import GenericViewSet

# Local
from .actions import SerializerMode


# --------------------------------------------------------------------------------
# > Mixins
# --------------------------------------------------------------------------------
class BrowsableMixin:
    """
    Explicitly blocks the "list" action to show the ViewSet in the browsable API
    (To be in the browsable API, a ViewSet must have either create() or list())
    """

    @staticmethod
    def list(request, *args, **kwargs):
        """
        Explicitly blocks the list() action
        :param HttpRequest request: The request object from django that called our action
        :param args: Additional args automatically passed to our action
        :param kwargs: Additional kwargs automatically passed to our action
        :return: HTTP error with code 405 because this method has been blocked
        :rtype: Response
        """
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


class ModelMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """Mixin that includes the 5 model mixins from DRF"""

    pass


# --------------------------------------------------------------------------------
# > Viewsets
# --------------------------------------------------------------------------------
class DynamicViewSet(GenericViewSet):
    """
    ---------- DESCRIPTION ----------
    Dynamic viewset that completely changes the way of writing DRF viewsets.
    It allows for more flexibility, better workflow control, and better code readability.
    Here are the major changes:
        You will no longer write actions within the viewset
        Instead, you will provide 2 dictionaries with settings, and actions will be generated from them
        For each action, you'll have to declare its ActionHandler class
        The ActionHandler will take care of processing the request/response
        Permissions are declared at 3 levels: global, viewset, and actions
        Permissions are cumulative: those 3 levels are merged with 'AND' relationships
        Serializers are declared in the ActionHandler and based on the action 'serializer_mode'

    Basically, your viewset should only contain:
        'known_actions'   -->     Dict for configuring the DRF known actions
        'extra_actions'   -->     Dict for configuring our custom actions
        helper and utility functions
    You technically CAN write actions normally in the viewset, but that defeat its purpose

    All actions will be generated and set on the viewset at the server start
    They will also be registered correctly in your DefaultRouter

    ---------- SETUP: known_actions ----------
    'known_actions' are the 6 already-existing actions of DRF (create, retrieve, ...)
    The dict should be a simple {name: {handler, permissions}} shape. Here's an example:
        {
            "create": {
                "handler": ActionHandler1,
                "permissions": (MyPermission, )
            }
            "list": {
                "handler": ActionHandler2,
                "permissions": (MyPermission, )
            }
        }

    ---------- SETUP: extra_actions ----------
    'extra_actions' are for custom actions, on which you'd typically used the @action decorator
    The dict will basically have to contain the handler and the decorator settings. Here's an example:
        {
            "report": {
                "handler": ActionHandler1,
                "permissions": (MyPermission,)
                "methods": ["post", "get"],
            },
            "postpone": {
                "handler": ActionHandler2,
                "permissions": (MyPermission,)
                "methods": ["post",],
                "url_path": "postponing",
                "detail": True,
            },
        }
    """

    viewset_permissions = None

    # --------------------------------------------------------------------------------
    # > Server setup
    # --------------------------------------------------------------------------------
    @classmethod
    def get_extra_actions(cls):
        """
        Methods automatically called by the DefaultRouter on server start to create the Routes of our viewset
        Overridden to first create and register all of our actions from the class configuration
        """
        cls._create_actions_from_config()
        return super().get_extra_actions()

    KNOWN_ACTION_NAMES = [
        "create",
        "list",
        "retrieve",
        "update",
        "partial_update",
        "destroy",
    ]

    known_actions = {}
    extra_actions = {}

    @classmethod
    def _create_actions_from_config(cls):
        """Dynamically creates and sets the ViewSet actions based on the class settings"""
        if hasattr(cls, "known_actions"):
            cls._create_known_actions_from_config()
        if hasattr(cls, "extra_actions"):
            cls._create_extra_actions_from_config()

    @classmethod
    def _create_known_actions_from_config(cls):
        """
        Dynamically creates and sets KNOWN actions based on the 'known_actions' attribute
        Please refer to the class docstring for more info on the 'known_actions' expected dict shape
        We use a sub-function to register each individual action due to closure/scope issues
        :raises ValueError: If the action name is not in the allowed names
        """
        for name, action_settings in cls.known_actions.items():
            if name not in cls.KNOWN_ACTION_NAMES:
                raise ValueError(
                    f"Invalid known action name '{name}'. Must be one of: {', '.join(cls.KNOWN_ACTION_NAMES)}"
                )

            cls._register_known_action(name, action_settings)

    @classmethod
    def _create_extra_actions_from_config(cls):
        """
        Dynamically creates and sets EXTRA actions based on the 'extra_actions' attribute
        Please refer to the class docstring for more info on the 'extra_actions' expected dict shape
        Each method must be configured with the right sub-attributes to match the DefaultRouter expectations
        We use a sub-function to register each individual action due to closure/scope issues
        :raises ValueError: If the name matches one of the allowed 'known' action names
        """
        for action_name, action_settings in cls.extra_actions.items():
            if action_name in cls.KNOWN_ACTION_NAMES:
                raise ValueError(
                    f"Invalid configuration: '{action_name}' action should be in the known_actions, not extra_actions"
                )
            cls._register_extra_action(action_name, action_settings)

    @classmethod
    def _register_known_action(cls, name, action_settings):
        """Registers an known action and setups its attributes"""
        detail = (
            True
            if name in {"retrieve", "update", "partial_update", "destroy"}
            else False
        )

        """Registers a known action, therefore skipping the @action decorator"""

        def action_method(self, request, *args, **kwargs):
            return self.call_action_handler(action_settings["handler"])

        setattr(cls, name, action_method)
        registered_action = getattr(cls, name)
        registered_action.permissions = action_settings.get("permissions", None)
        registered_action.detail = detail
        registered_action.__name__ = name

    @classmethod
    def _register_extra_action(cls, action_name, action_settings):
        """Registers an extra action using the @action decorator and setups its attributes"""
        # Prepare the action decorator
        detail = action_settings.get("detail", False)
        decorator_kwargs = {
            "name": action_name,
            "url_name": action_settings.get("url_name", action_name),
            "url_path": action_settings.get("url_path", action_name),
            "methods": action_settings.get("methods", None),
            "detail": detail,
        }

        # Create the handler
        @action(**decorator_kwargs)
        def action_method(self, request, *args, **kwargs):
            handler_class = action_settings["handler"]
            return self.call_action_handler(handler_class)

        # Register and configure the method for the router
        setattr(cls, action_name, action_method)
        registered_action = getattr(cls, action_name)
        registered_action.__name__ = action_name
        registered_action.mapping = {}
        registered_action.detail = detail
        registered_action.permissions = action_settings.get("permissions", None)
        registered_action.mapping = MethodMapper(
            registered_action, decorator_kwargs["methods"]
        )

    # --------------------------------------------------------------------------------
    # > Action Permissions
    # --------------------------------------------------------------------------------
    def check_permissions(self, request):
        """
        Adds the 'is_detail_action' boolean to the request before checking the permissions
        Useful for our custom permissions that may be restricted to "detail" actions
        The 'action' might be None when checking the DRF API interface
        :param Request request: The request object from the API call
        """
        if self.action is not None:
            action_method = getattr(self, self.action)
            request.is_detail_action = action_method.detail
        super().check_permissions(request)

    def get_permissions(self):
        """
        Overridden to dynamically get the permission list based on the action called
        It fetches permissions from 3 different spots:
            Global permissions set in the settings
            Viewset permissions set in our current ViewSet
            Action permissions set in our ActionHandler
        Those 3 lists are then merged together with an 'AND' relation
        If no permission is found, we use the default one
        :return: List of permission INSTANCES for our action
        :rtype: list(Permission)
        """
        global_permissions = self._get_global_permissions()
        viewset_permissions = self._get_viewset_permissions()
        action_permissions = self._get_action_permissions()
        permissions = (
            list(global_permissions)
            + list(viewset_permissions)
            + list(action_permissions)
        )
        if len(permissions) == 0:
            permissions = api_settings.DEFAULT_PERMISSION_CLASSES
        permissions = list(set(permissions))
        return [permission() for permission in permissions]

    @staticmethod
    def _get_global_permissions():
        """
        Fetches the global permission list declared in the settings
        Note that those permissions are strings that must be turned into class
        :return: List of permission CLASSES apply to the entire application
        :rtype: list(Permission)
        """
        permissions = getattr(settings, "DRF_GLOBAL_PERMISSIONS", None)
        if permissions is None:
            return []
        else:
            return [import_string(permission) for permission in permissions]

    def _get_viewset_permissions(self):
        """
        Fetches the viewset-wide permissions declared in our action's viewset
        :return: List of permission CLASSES for our viewset
        :rtype: list(Permission)
        """
        permissions = getattr(self, "viewset_permissions", None)
        if permissions is None:
            permissions = []
        return permissions

    def _get_action_permissions(self):
        """
        Fetches the permissions attached to our action handler
        This forces developers to explicitly state permissions for actions
        :return: List of permission CLASSES for our action
        :rtype: list(Permission)
        """
        permissions = []
        if self.action is not None:
            handler = getattr(self, self.action)
            if handler.permissions:
                permissions = handler.permissions
        return permissions

    # --------------------------------------------------------------------------------
    # > Action Serializers
    # --------------------------------------------------------------------------------
    def get_serializer_class(self):
        """
        Overridden to dynamically get the permission list based on the action and the method
        It will be retrieved from the corresponding ActionHandler class, in its 'serializer' attribute.
        There are 4 possible shapes for the "serializer" attribute:
            NONE                    returns None
            UNIQUE                  directly returns a serializer
            METHOD_BASED            dict where each method has a serializer
            ROLE_BASED              dict with a different serializer for "user" and for "admin"
            ROLE_AND_METHOD_BASED   dict with user/admin, then methods for serializers
        :raises ValueError: When you do not provide a valid serializer mode in the action handler
        :return: Serializer class attached for our action
        :rtype: Serializer or None
        """
        handler_class = self._get_handler_class(self.action)
        user_type = "admin" if self.request.user.is_staff else "user"
        method = self.request.method.lower()
        mode = handler_class.serializer_mode
        # Fetches the serializer based on the 'serializer_mode'
        if mode == SerializerMode.NONE:
            return None
        elif mode == SerializerMode.UNIQUE:
            return handler_class.serializer
        elif mode == SerializerMode.METHOD_BASED:
            return handler_class.serializer[method]
        elif mode == SerializerMode.ROLE_BASED:
            return handler_class.serializer[user_type]
        elif mode == SerializerMode.ROLE_AND_METHOD_BASED:
            return handler_class.serializer[user_type][method]
        else:
            raise ValueError(f"Invalid 'serializer_mode' for {handler_class.__name__}")

    def get_valid_serializer(self, *args, **kwargs):
        """
        Shortcut to fetch the serializer, try to validate its data, and return it
        :param args: Additional args for creating the serializer
        :param kwargs: Additional kwargs for creating the serializer
        :return: The validated serializer instance
        :rtype: Serializer
        :raises ValidationError: If the serializer is not valid
        """
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer

    # --------------------------------------------------------------------------------
    # > Other Action Helpers
    # --------------------------------------------------------------------------------
    def call_action_handler(self, handler_class):
        """
        Creates an ActionHandler instance with the initial arguments and runs it
        :param ActionHandler handler_class: ActionHandler class in charge of processing the action-method
        :return: Response object from DRF, generated by processing our action
        :rtype: Response
        """
        action_handler = handler_class(self, self.request, *self.args, **self.kwargs)
        return action_handler.run()

    @classmethod
    def _get_handler_class(cls, action_name):
        """
        Fetches the ActionHandler class attached to our endpoind (action+method), based on the viewset settings
        :return: The ActionHandler for this endpoint
        :rtype: ActionHandler
        """
        attribute = (
            "known_actions"
            if action_name in cls.KNOWN_ACTION_NAMES
            else "extra_actions"
        )
        settings = getattr(cls, attribute).get(action_name, {})
        return settings["handler"]


class DynamicModelViewSet(DynamicViewSet, ModelMixin):
    """DynamicViewSet with built-in CRUD actions"""

    pass
