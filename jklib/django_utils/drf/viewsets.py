"""Viewset and mixin classes for DRF"""

# Django
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.viewsets import GenericViewSet


class BulkDestroyMixin:
    """Mixin to delete multiple instances at once"""

    def bulk_destroy(self, request: Request) -> Response:
        """Delete multiple instances at once"""
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
    BulkDestroyMixin,
    mixins.ListModelMixin,
):
    """Mixin that includes the 5 model mixins from DRF"""

    pass


class ImprovedViewSet(GenericViewSet):
    """
    Extends GenericViewSet to provide more flexibility on action settings
    Permissions:
        It uses permissions from 3 different settings:
        - global:       settings.DRF_GLOBAL_PERMISSION_CLASSES
        - viewset:      YourViewSet.viewset_permission_classes
        - action:       YourViewSet.permission_classes[action]
    Serializers:
        The serializer is action-based: YourViewSet.serializer_classes[action]
    """

    KNOWN_ACTIONS_DETAIL_MAP = {
        "create": False,
        "list": False,
        "retrieve": True,
        "update": True,
        "partial_update": True,
        "destroy": True,
        "bulk_destroy": False,
    }

    viewset_permission_classes = ()
    permission_classes = {}
    serializer_classes = {}

    # ----------------------------------------
    # Permissions
    # ----------------------------------------
    def check_permissions(self, request):
        """
        Overridden to add the 'is_detail_action' boolean to the request beforehand
        :param Request request: The request object from the API call
        """
        if self.action is not None:
            if self.action in self.KNOWN_ACTIONS_DETAIL_MAP:
                is_detail = self.KNOWN_ACTIONS_DETAIL_MAP[self.action]
            else:
                action_method = getattr(self, self.action)
                is_detail = action_method.detail
            request.is_detail_action = is_detail
        super().check_permissions(request)

    def get_permissions(self):
        """
        Merges permissions with `AND` from 3 spots: global, viewset, and action
        :return: List of permission instances for our action
        :rtype: list(Permission)
        """
        # Action permissions
        permissions_map = getattr(self, "permission_classes", {})
        default_permission_classes = permissions_map.get("default", None)
        action_permission_classes = permissions_map.get(
            self.action, default_permission_classes
        )
        if action_permission_classes is None:
            action_permission_classes = []
        # Viewset permissions
        viewset_permission_classes = getattr(self, "viewset_permission_classes", None)
        if viewset_permission_classes is None:
            viewset_permission_classes = []
        # Global permissions
        global_permission_classes = [
            import_string(permission)
            for permission in getattr(settings, "DRF_GLOBAL_PERMISSION_CLASSES", [])
        ]
        if global_permission_classes is None:
            global_permission_classes = []
        # Merge permissions
        permissions = (
            list(global_permission_classes)
            + list(viewset_permission_classes)
            + list(action_permission_classes)
        )
        if len(permissions) == 0:
            permissions = api_settings.DEFAULT_PERMISSION_CLASSES
        permissions = list(set(permissions))
        return [permission() for permission in permissions]

    # ----------------------------------------
    # Serializers
    # ----------------------------------------
    def get_serializer_class(self):
        """
        Fetches the action serializer using the `serializer_classes` map
        :return: Serializer class attached for our action
        :rtype: Serializer or None
        """
        serializers_map = getattr(self, "serializer_classes", {})
        default_serializer_class = serializers_map.get("default", None)
        action_serializer_class = serializers_map.get(
            self.action, default_serializer_class
        )
        return action_serializer_class

    def get_valid_serializer(self, *args, **kwargs):
        """
        Shortcut to fetch the serializer, try to validate its data, and return it
        :param args: Additional args for creating the serializer
        :param kwargs: Additional kwargs for creating the serializer
        :return: The validated serializer instance
        :rtype: Serializer
        :raise ValidationError: If the serializer is not valid
        """
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class ImprovedModelViewSet(ImprovedViewSet, ModelMixin):
    """ImprovedViewSet with built-in CRUD actions"""

    pass
