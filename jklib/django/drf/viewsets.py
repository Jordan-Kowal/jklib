# coding: utf-8
"""
Description:
    Contains custom mixins, views, and viewsets for our API
Mixins:
    DynamicPermissionsMixin: Mixin to make the permissions dynamic, based on the action
    DynamicSerializersMixin: Mixin to make the serializers dynamic, based on the action
    ModelMixin: Mixin that includes the 5 model mixins from DRF
    ShowAsBrowsableMixin: Explicitly blocks the "list" action to show the ViewSet in the browsable API
Viewsets:
    DynamicViewSet: GenericViewSet from DRF with dynamic handling of serializers and permissions
    ModelViewSet: Dynamic viewset for Django models which includes the basic CRUD
Views:
    improved_list_view: Improved LIST action which filters and sorts data using GET parameters
"""


# Django
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

# Personal
from jklib.django.models.queries import filter_on_text, single_sort_by

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


# --------------------------------------------------------------------------------
# > ViewSets
# --------------------------------------------------------------------------------
class DynamicViewSet(
    DynamicPermissionsMixin, DynamicSerializersMixin, viewsets.GenericViewSet
):
    """
    GenericViewSet from DRF with dynamic handling of serializers and permissions
    Provides some utility as well
    """

    def get_valid_serializer(self, *args, **kwargs):
        """Gets the serializer and checks if it is valid"""
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class ModelViewSet(DynamicViewSet, ModelMixin):
    """Dynamic viewset for Django models which includes the basic CRUD"""

    pass


# --------------------------------------------------------------------------------
# > Views
# --------------------------------------------------------------------------------
def improved_list_view(viewset, *searchable_fields):
    """
    Improved LIST action which filters and sorts data using GET parameters
    Accepted parameters are:
        sort_by     Will order the results with the given column name
        ascending   Impact to sort order
        search      Check if fields contain this value (must be at least 3 char long)
        page        The page number you want to get
        page_size   The amount of element per page
    """
    # Initial state
    queryset = viewset.filter_queryset(viewset.get_queryset())
    get_params = viewset.request.query_params
    # Filter results
    search = get_params.get("search", "")
    queryset = filter_on_text(queryset, search, 3, *searchable_fields)
    queryset = single_sort_by(queryset, get_params)
    # Paginate if available
    page = viewset.paginate_queryset(queryset)
    if page is not None:
        serializer = viewset.get_serializer(page, many=True)
        return viewset.get_paginated_response(serializer.data)
    # Return results
    serializer = viewset.get_serializer(queryset, many=True)
    return Response(serializer.data)
