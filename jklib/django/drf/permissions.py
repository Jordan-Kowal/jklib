"""Permission classes for DRF"""


# Django
from rest_framework.permissions import BasePermission


# --------------------------------------------------------------------------------
# > Permissions
# --------------------------------------------------------------------------------
class BlockAll(BasePermission):
    """Blocks all incoming traffic"""

    message = "Access denied"

    @staticmethod
    def has_permission(request, view):
        """Always denied"""
        return False

    @staticmethod
    def has_object_permission(request, view, obj):
        """Always denied"""
        return False


class IsNotAuthenticated(BasePermission):
    """User must be disconnected"""

    message = "You must logout to access this service"

    @staticmethod
    def has_permission(request, view):
        """Returns true if user is not logged in"""
        authenticated = request.user.is_authenticated
        return not authenticated


class IsNotVerified(BasePermission):
    """User must be authenticated but not yet verified"""

    message = "Your account must not be verified"

    @staticmethod
    def has_permission(request, view):
        """Returns True if user is logged in and not verified"""
        user = request.user
        if not user.is_authenticated:
            return False
        profile = user.profile
        if profile.is_verified:
            return False
        return True


class IsObjectOwner(BasePermission):
    """Object must be attached to the user, or be the user itself"""

    message = "Access denied"

    # TODO: Include other fieldnames life create_by, owner, owned_by
    @staticmethod
    def has_object_permission(request, view, obj):
        """Checks if user is owner or is object"""
        user = request.user
        # Getting the owner
        try:
            owner = obj.user
        except AttributeError:
            owner = None
        # Assertion
        if owner:
            return owner == user
        else:
            return obj == user


class IsVerified(BasePermission):
    """User must be authenticated but not yet verified"""

    message = "Your account must be verified"

    @staticmethod
    def has_permission(request, view):
        """Returns True if user is logged in and not verified"""
        user = request.user
        if not user.is_authenticated:
            return False
        profile = user.profile
        if profile.is_verified:
            return True
        return False
