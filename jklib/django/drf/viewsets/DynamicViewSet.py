"""DynamicViewSet"""


# Django
from rest_framework import status, viewsets

# Local
from ..mixins import DynamicPermissionsMixin, DynamicSerializersMixin


class DynamicViewSet(
    DynamicPermissionsMixin, DynamicSerializersMixin, viewsets.GenericViewSet
):
    """
    GenericViewSet from DRF with the following improvements:
        Dynamic serializers (1 per action)
        Dynamic permissions (1 list per action)
        Methods to interact with our Action classes
        Various utility methods
    """

    def get_valid_serializer(self, *args, **kwargs):
        """Gets the serializer and checks if it is valid"""
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer

    def run_action(self, action_class):
        """
        Creates an Action instance with the initial arguments and runs its "process" method
        Args:
            action_class (Action): Action class that inherits from our BaseAction class
        Returns:
            (HttpResponse): Response from the service
        """
        action_instance = action_class(self, self.request, *self.args, **self.kwargs)
        return action_instance.run()
