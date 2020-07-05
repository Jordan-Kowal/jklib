"""
Viewset and mixin classes for DRF
Split into sub-categories:
    Mixins: Provide utility functions for viewsets (but do not inherit from them)
    Viewsets: Improved DRF ViewSets through custom mixins and utility functions
"""


# Django
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

# Local
from .permissions import BlockAll


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
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
class DynamicViewSet(viewsets.GenericViewSet):
    """
    ---------- DESCRIPTION ----------
    Dynamic viewset that completely changes the way of writing DRF viewsets.
    It allows for more flexibility, better workflow control, and better code readability.
    Here are the major changes:
        You will no longer write actions within the viewset
        Instead, you will provide 2 dictionaries with settings, and actions will be generated from them
        For each action, you'll have to declare its ActionHandler class
        The ActionHandler will take care of processing the request/response
        Permissions and serializers will be fetched from the ActionHandler
        They both can be set at the method level (post, get, etc.)

    Basically, your viewset should only contain:
        'known_actions'   -->     Dict for configuring the DRF known actions
        'extra_actions'   -->     Dict for configuring our custom actions
        helper and utility functions
    You technically CAN write actions normally in the viewset, but that defeat its purpose

    All actions will be generated and set on the viewset at the server start
    They will also be registered correctly in your DefaultRouter

    ---------- SETUP: known_actions ----------
    'known_actions' are the 6 already-existing actions of DRF (create, retrieve, ...)
    The dict should be a simple {name: handler} shape. Here's an example:
        {
            "create": ActionHandler1,
            "list": ActionHandler2,
        }

    ---------- SETUP: extra_actions ----------
    'extra_actions' are for custom actions, on which you'd typically used the @action decorator
    The dict will basically have to contain the handler and the decorator settings. Here's an example:
        {
            "report": {
                "handler": ActionHandler1,
                "methods": ["post", "get"],
            },
            "postpone": {
                "handler": ActionHandler2,
                "methods": ["post",],
                "url_path": "postponing",
                "detail": True,
            },
        }
    """

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
        Because these are KNOWN actions, we cannot use the @action decorator
        Please refer to the class docstring for more info on the 'known_actions' expected dict shape
        """
        for name, handler_class in cls.model_actions.items():
            # Check the reserved names
            if name not in cls.KNOWN_ACTION_NAMES:
                raise ValueError(
                    f"Invalid known action name '{name}'. Must be one of: {', '.join(cls.KNOWN_ACTION_NAMES)}"
                )

            # Create the handler
            def action_method(self, request, *args, **kwargs):
                self.call_action_handler(handler_class)

            # Register and configure the method for the router
            setattr(cls, name, action_method)
            registered_action = getattr(cls, name)
            registered_action.__name__ = name

    @classmethod
    def _create_extra_actions_from_config(cls):
        """
        Dynamically creates and sets EXTRA actions based on the 'extra_actions' attribute
        Please refer to the class docstring for more info on the 'extra_actions' expected dict shape
        Each method must be configured with the right sub-attributes to match the DefaultRouter expectations
        """
        for action_name, action_settings in cls.extra_actions.items():
            # Check the reserved names
            if action_name in cls.KNOWN_ACTION_NAMES:
                raise ValueError(
                    f"Invalid configuration: '{action_name}' action should be in the known_actions, not extra_actions"
                )

            # Prepare the @action decorator
            action_params = {
                "name": action_name,
                "url_name": action_settings.get("url_name", action_name),
                "url_path": action_settings.get("url_path", None),
                "methods": action_settings.get("methods", None),
                "detail": action_settings.get("detail", False),
            }

            # Create the handler
            @action(**action_params)
            def action_method(self, request, *args, **kwargs):
                handler_class = action_settings["handler"]
                self.call_action_handler(handler_class)

            # Register and configure the method for the router
            setattr(cls, action_name, action_method)
            registered_action = getattr(cls, action_name)
            registered_action.__name__ = action_name
            registered_action.mapping = {}
            for method in action_params["methods"]:
                registered_action.mapping[method] = action_name

    # --------------------------------------------------------------------------------
    # > For action calls
    # --------------------------------------------------------------------------------
    def get_permissions(self):
        """
        Overridden to dynamically get the permission list based on the action and the method
        It will be retrieved from the corresponding ActionHandler class, in its 'permissions' attribute.
        It can either be:
            permissions = (Permission1, ...)
            permissions = {'get': (Permission1, ...), 'post': (Permission1, ...), ...}
        Only valid permission classes will be returned, and it defaults to [BlockAll()]
        :return: List of permission instances for our action
        :rtype: list(Permission)
        """
        default_permission = BlockAll

        # If no handler, we block all incoming traffic
        handler_class = self._get_handler_class(self.action)
        if handler_class is None:
            return [default_permission()]

        # Fetch the permissions
        permissions = getattr(handler_class, "permissions", [default_permission])
        if type(permissions) in [list, tuple]:
            pass
        elif type(permissions) == dict:
            method = self.method.lower()
            permissions = permissions.get(method, [default_permission])
        else:
            permissions = [default_permission]

        # Keep only actual Permission classes
        valid_permissions = [
            cls for cls in permissions if issubclass(cls, BasePermission)
        ]
        if len(valid_permissions) == 0:
            return [default_permission()]
        return [permission() for permission in valid_permissions]

    def get_serializer_class(self):
        """
        Overridden to dynamically get the permission list based on the action and the method
        It will be retrieved from the corresponding ActionHandler class, in its 'serializers' attribute.
            serializers = Serializer1
            serializers = {'get': Serializer1, 'post': Serializer2, ...}
        If no serializer class is found, returns None
        :return: Serializer class attached for our action
        :rtype: Serializer or None
        """
        # If no handler, we block all incoming traffic
        handler_class = self._get_handler_class(self.action)
        if handler_class is None:
            return None

        # Fetch the serializer
        serializer = handler_class.serializer
        if type(serializer) == dict:
            method = self.method.lower()
            serializer = serializer.get(method, None)

        # Check if it is an actual serializer
        if issubclass(serializer, BaseSerializer):
            return serializer
        return None

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
        Fetches the ActionHandler class attached to our action, base on the viewset settings
        :return:
        """
        if action_name in cls.KNOWN_ACTION_NAMES:
            return cls.known_actions.get(action_name, None)
        else:
            action_settings = cls.extra_actions.get(action_name, {})
            return action_settings.get("handler", None)


class DynamicModelViewSet(DynamicViewSet, ModelMixin):
    """DynamicViewSet with built-in CRUD actions"""

    pass
