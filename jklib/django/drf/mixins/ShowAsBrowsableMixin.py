"""ShowAsBrowsableMixin"""


# Django
from rest_framework import status
from rest_framework.response import Response


class ShowAsBrowsableMixin:
    """
    Explicitly blocks the "list" action to show the ViewSet in the browsable API
    (To be in the browsable API, a ViewSet must have either create() or list())
    """

    @staticmethod
    def list(request, *args, **kwargs):
        """
        Registers and explicitly blocks the list() action
        Returns:
            (HttpResponse) Response from DRF with 405 status code
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
