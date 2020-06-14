"""DynamicViewSet"""


# Django
from rest_framework import status, viewsets

# Local
from ..mixins import DynamicPermissionsMixin, DynamicSerializersMixin


class DynamicViewSet(
    DynamicPermissionsMixin, DynamicSerializersMixin, viewsets.GenericViewSet
):
    """
    GenericViewSet from DRF with dynamic handling of serializers and permissions
    Provides functions to interact with our Service class and other various utility functions
    """

    def get_valid_serializer(self, *args, **kwargs):
        """Gets the serializer and checks if it is valid"""
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer

    def call_service(self, service_class):
        """
        Creates a Service instance with the initial arguments and runs its "process" method
        Args:
            service_class (Service): Service class from the "service.py" file
        Returns:
            (HttpResponse): Response from the service
        """
        service_instance = service_class(self, self.request, *self.args, **self.kwargs)
        return service_instance.process()
