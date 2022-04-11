"""Viewset and mixin classes for DRF."""

# Built-in
from typing import Any, Dict, List, Optional, Tuple, Type

# Django
from rest_framework import mixins
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.viewsets import GenericViewSet


class BulkDestroyMixin:
    """Mixin to delete multiple instances at once."""

    def bulk_destroy(self, request: Request) -> Response:
        """Delete multiple instances at once."""
        serializer = self.get_valid_serializer(data=request.data)  # type: ignore
        ids_to_delete = serializer.validated_data.pop("ids")
        instances = self.get_queryset().filter(id__in=ids_to_delete)  # type: ignore
        if len(instances) == 0:
            return Response(None, status=HTTP_404_NOT_FOUND)
        else:
            instances.delete()
            return Response(None, status=HTTP_204_NO_CONTENT)


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

    default_permissions: Tuple[Type[BasePermission]] = ()  # type: ignore
    default_serializer: Optional[Type[BaseSerializer]] = None
    permissions_per_action: Dict[str, Tuple[Type[BasePermission]]] = {}
    serializer_per_action: Dict[str, Type[BaseSerializer]] = {}

    def get_permissions(self) -> List[BasePermission]:
        """Override.

        Either gets the action permission s, viewset permissions, or
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
        serializer = self.serializer_per_action.get(
            self.action, self.default_serializer
        )
        if serializer is None:
            raise RuntimeError(f"Serializer not found for action '{self.action}'")
        return serializer

    def get_valid_serializer(self, *args: Any, **kwargs: Dict) -> BaseSerializer:
        """Shortcut to fetch the serializer, try to validate its data, and
        return it."""
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class ImprovedModelViewSet(ImprovedViewSet, ModelMixin):
    pass
