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

    default_permission_classes: Sequence[Type[BasePermission]] = ()
    default_serializer_class: Optional[Type[BaseSerializer]] = None
    permission_classes_per_action: Dict[str, Sequence[Type[BasePermission]]] = {}
    serializer_class_per_action: Dict[str, Type[BaseSerializer]] = {}

    def get_permissions(self) -> List[BasePermission]:
        permissions = self.permission_classes_per_action.get(
            self.action, self.default_permission_classes
        )
        if len(permissions) == 0:
            permissions = api_settings.DEFAULT_PERMISSION_CLASSES
        return [permission() for permission in permissions]

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.serializer_class_per_action.get(
            self.action, self.default_serializer_class
        )

    def get_valid_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer:
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer
