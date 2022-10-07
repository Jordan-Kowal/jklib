"""Permission classes for DRF."""


# Django
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class BlockAll(BasePermission):
    """Blocks all incoming traffic.

    Equivalent to ~AllowAny, but makes it explicit
    """

    message = "Access denied"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Always denied."""
        return False


class IsNotAuthenticated(BasePermission):
    """User must be disconnected."""

    message = "You must be logged out to use this service"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Literally the opposite of IsAuthenticated."""
        return not super().has_permission(request, view)
