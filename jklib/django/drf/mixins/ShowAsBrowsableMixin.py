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
        """Explicitly block the list() action"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
