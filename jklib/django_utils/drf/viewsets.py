"""Viewset and mixin classes for DRF."""

# Built-in
from typing import Any, Dict, List, Optional, Sequence, Type

# Django
from rest_framework import mixins
from rest_framework.permissions import BasePermission
from rest_framework.serializers import BaseSerializer
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class ModelMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    pass


class ImprovedViewSet(GenericViewSet):
    """Allow permissions and serializers to be 'per action'."""

    default_permissions: Sequence[Type[BasePermission]] = ()
    default_serializer: Optional[Type[BaseSerializer]] = None
    permissions_per_action: Dict[str, Sequence[Type[BasePermission]]] = {}
    serializer_per_action: Dict[str, Type[BaseSerializer]] = {}

    def get_permissions(self) -> List[BasePermission]:
        """Override.

        Either gets the action permissions, viewset permissions, or
        default settings permissions
        """
        permissions = self.permissions_per_action.get(
            self.action, self.default_permissions
        )
        if len(permissions) == 0:
            permissions = api_settings.DEFAULT_PERMISSION_CLASSES
        return [permission() for permission in permissions]

    def get_serializer_class(self) -> Type[BaseSerializer]:
        """Override.

        Fetches the action serializer using the `serializer_classes` map
        """
        return self.serializer_per_action.get(self.action, self.default_serializer)

    def get_valid_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer:
        """Shortcut to fetch the serializer, try to validate its data, and
        return it."""
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class ImprovedModelViewSet(ImprovedViewSet, ModelMixin):
    pass
