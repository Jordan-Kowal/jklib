"""
Description:
    Contains mixins that can be used in viewsets
Mixins:
    DynamicPermissionsMixin: Mixin to make the permissions dynamic, based on the action
    DynamicSerializersMixin: Mixin to make the serializers dynamic, based on the action
    ModelMixin: Mixin that includes the 5 model mixins from DRF
    ShowAsBrowsableMixin: Explicitly blocks the "list" action to show the ViewSet in the browsable API
"""

# Django
from rest_framework import mixins, status
from rest_framework.response import Response

# Local
from .permissions import BlockAll


# --------------------------------------------------------------------------------
# > Mixins
# --------------------------------------------------------------------------------
class DynamicPermissionsMixin:
    """
    Mixin to make the permissions dynamic, based on the action
    'permission_class' becomes useless and we will instead use [action].permissions
    """

    def get_permissions(self):
        """
        Overrides the method to fetch permissions in [action].permissions
        If permissions are forgotten, defaults to "BlockAll" to avoid security breaches
        """
        if self.action is None:
            permissions = [BlockAll]
        else:
            action_object = getattr(self, self.action)
            permissions = getattr(action_object, "permissions", [BlockAll])
        return [permission() for permission in permissions]


class DynamicSerializersMixin:
    """
    Mixin to make the serializers dynamic, based on the action
    'serializer_classes' becomes useless and we will instead use [action].serializer
    """

    def get_serializer_class(self, *args, **kwargs):
        """Overridden to dynamically get the serializer from [action].serializer"""
        action_object = getattr(self, self.action)
        serializer_class = action_object.serializer
        return serializer_class


class ModelMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """Mixin that includes the 5 model mixins from DRF"""

    pass


class ShowAsBrowsableMixin:
    """
    Explicitly blocks the "list" action to show the ViewSet in the browsable API
    (To be in the browsable API, a ViewSet must have either create() or list())
    """

    @staticmethod
    def list(request, *args, **kwargs):
        """Explicitly block the list() action"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
