"""
Viewset and mixin classes for DRF
Split into sub-categories:
    Mixins: Provide utility functions for viewsets (but do not inherit from them)
    Viewsets: Improved DRF ViewSets through custom mixins and utility functions
"""


# Django
from rest_framework import mixins, status, viewsets
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


class DynamicPermissionsMixin:
    """
    Mixin to make the permissions dynamic, based on the action and the method
    'permission_class' becomes useless and we will instead use:
        [action].permissions
        [action].permissions[method]
    """

    def get_permissions(self):
        """
        Overridden to dynamically get the permission list based on the action and the method
        Will look for and return a permissions classes in [action].permissions or [action].permissions[method]
        Returns only valid permissions classes, and defaults to [BlockAll()]
        :return: List of permission instances attached to our action
        :rtype: list(Permission)
        """
        default_permission = BlockAll
        if self.action is None:
            return [default_permission()]
        action_object = getattr(self, self.action)
        permissions = getattr(action_object, "permissions", [default_permission])
        # We have a list of permissions
        if type(permissions) == list:
            permissions = [
                cls for cls in permissions if issubclass(cls, BasePermission)
            ]
        # We have a dict and expect permissions to be in method keys
        elif type(permissions) == dict:
            method = self.method.lower()
            permissions = permissions.get(method, [BlockAll])
            permissions = [
                cls for cls in permissions if issubclass(cls, BasePermission)
            ]
        # Unexpected format
        else:
            permissions = [default_permission]
        return [permission() for permission in permissions]


class DynamicSerializersMixin:
    """
    Mixin to make the serializers dynamic, based on the action and the method
    'serializer_classes' becomes useless and we will instead use:
        [action].serializer
        [action].serializer[method]
    """

    def get_serializer_class(self):
        """
        Overridden to dynamically get the serializer based on the action and the method
        Will look for and return a serializer class in [action].serializer or [action].serializer[method]
        If no serializer class is found, returns None
        :return: Serializer class attached to our action
        :rtype: Serializer or None
        """
        if self.action is None:
            return None
        action_object = getattr(self, self.action)
        serializer = action_object.serializer
        # We found the serializer
        if issubclass(serializer, BaseSerializer):
            return serializer
        # We have a dict and expect permissions to be in method keys
        elif type(serializer) == dict:
            method = self.method.lower()
            serializer_class = serializer.get(method, None)
            if issubclass(serializer_class, BaseSerializer):
                return serializer_class
            return None
        # Unexpected format
        else:
            return None


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
class DynamicViewSet(
    DynamicPermissionsMixin, DynamicSerializersMixin, viewsets.GenericViewSet
):
    """
    GenericViewSet from DRF with the following improvements:
        Dynamic serializers (1 per action-method)
        Dynamic permissions (1 list per action-method)
        Methods to interact with our Action classes
        Various utility methods
    """

    def get_valid_serializer(self, *args, **kwargs):
        """
        Gets the serializer attached to our action-method and checks if it is valid
        Then returns the validated serializer instance
        :param args: Additional args for creating the serializer
        :param kwargs: Additional kwargs for creating the serializer
        :return: The validated serializer instance
        :rtype: Serializer
        :raises ValidationError: If the serializer is not valid
        """
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer

    def run_action(self, action_class):
        """
        Creates an Action instance with the initial arguments and runs it
        :param BaseAction action_class: Action class in charge of processing the action-method
        :return: Response object from DRF, generated by processing our action
        :rtype: Response
        """
        action_instance = action_class(self, self.request, *self.args, **self.kwargs)
        return action_instance.run()


class DynamicModelViewSet(DynamicViewSet, ModelMixin):
    """DynamicViewSet with built-in CRUD actions"""

    pass
