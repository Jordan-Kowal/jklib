from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


class BlockAll(BasePermission):
    """Blocks all requests."""

    message = "Access denied"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return False


class IsNotAuthenticated(IsAuthenticated):
    """Blocks requests if the user is authenticated."""

    message = "You must be logged out to use this service"

    def has_permission(self, request: Request, view: APIView) -> bool:
        return not super().has_permission(request, view)
