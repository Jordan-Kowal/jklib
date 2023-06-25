# Built-in
from typing import Any, Dict, Generator, List, Optional, Sequence, Type

# Django
from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import BaseSerializer, Serializer
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class ModelMixin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """A mixin that includes all the `ModelMixin`s."""

    pass


class ImprovedViewSet(GenericViewSet):
    """Allows permissions and serializers to be 'per action'."""

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

    def generate_json_streaming_content(
        self,
        queryset: QuerySet,
        serializer_class: Optional[Type[Serializer]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Generator[bytes, None, None]:
        """Generates a JSON streaming response as bytes from a queryset."""
        serializer_class = serializer_class or self.get_serializer_class()
        context = context or self.get_serializer_context()
        renderer = JSONRenderer()
        total = queryset.count()
        # Manually adds [] and , to the response to make it a valid JSON array
        for i, item in enumerate(queryset):
            data = b""
            if i == 0:
                data += b"["
            serializer = serializer_class(item, context=context)
            data += renderer.render(serializer.data)
            if i == total - 1:
                data += b"]"
            else:
                data += b","
            yield data
