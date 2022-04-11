"""Permission classes for DRF."""


# Django
from django.db.models import Model
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class UserPermissionMixin:
    """Provides utilities for user-related permissions."""

    def is_object_owner(self, request: Request, obj: Model) -> bool:
        """Checks if the user is or owns the object."""
        try:
            return (
                self.user_is_valid(request)
                and request.user.is_authenticated
                and (request.user == obj or request.user == obj.user)
            )
        except AttributeError:
            return False

    @staticmethod
    def user_is_valid(request: Request) -> bool:
        """Checks if the user is valid."""
        return bool(request.user) and bool(request.user.id)


class IsAdminOrOwner(UserPermissionMixin, BasePermission):
    """Equivalent to the following permission: (IsObjectOwner |
    IsAdminUser,)"""

    message = "Access denied"

    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        """User must either be the owner or an admin."""
        is_admin = bool(self.user_is_valid(request) and request.user.is_staff)
        return self.is_object_owner(request, obj) or is_admin


class BlockAll(UserPermissionMixin, BasePermission):
    """Blocks all incoming traffic.

    Equivalent to ~AllowAny, but makes it explicit
    """

    message = "Access denied"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Always denied."""
        return False


class IsNotAuthenticated(UserPermissionMixin, BasePermission):
    """User must be disconnected.

    Equivalent to ~IsAuthenticated, but makes it explicit
    """

    message = "You must logout to access this service"

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Returns true if user is not logged in."""
        return not bool(self.user_is_valid(request) and request.user.is_authenticated)


class IsObjectOwner(UserPermissionMixin, BasePermission):
    """Object must be attached to the user, or be the user itself."""

    message = "Access denied"

    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        """Checks if user is owner or is object."""
        return self.is_object_owner(request, obj)


class IsSuperUser(UserPermissionMixin, BasePermission):
    """Allows access only to superusers."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Returns whether the user is a superuser."""
        return bool(self.user_is_valid(request) and request.user.is_superuser)
