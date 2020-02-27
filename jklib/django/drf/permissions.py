# coding: utf-8
"""
Description:
    Custom permission classes used throughout the API
Permissions:
    BlockAll: Blocks all incoming traffic
    IsOwner: Object must be attached to the user, or be the user itself
    IsNotAuthenticated: User must be disconnected
    IsNotVerified: User must be authenticated but not yet verified
    IsVerified: User must be authenticated and flagged as 'verified'
"""

# Django
from rest_framework import permissions


# --------------------------------------------------------------------------------
# > Permissions
# --------------------------------------------------------------------------------
class BlockAll(permissions.BasePermission):
    """Blocks all incoming traffic"""

    message = "Accès refusé pour tous"

    def has_permission(self, request, view):
        """Always denied"""
        return False

    def has_object_permission(self, request, view, obj):
        """Always denied"""
        return False


class IsObjectOwner(permissions.BasePermission):
    """Object must be attached to the user, or be the user itself"""

    message = "Vous n'êtes pas le propriétaire"

    def has_object_permission(self, request, view, obj):
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


class IsNotAuthenticated(permissions.BasePermission):
    """User must be disconnected"""

    message = "Vous devez vous déconnecter"

    def has_permission(self, request, view):
        """Returns true if user is not logged in"""
        authenticated = request.user.is_authenticated
        return not authenticated


class IsNotVerified(permissions.BasePermission):
    """User must be authenticated but not yet verified"""

    message = "Ce compte a déjà été vérifié"

    def has_permission(self, request, view):
        """Returns True if user is logged in and not verified"""
        user = request.user
        if not user.is_authenticated:
            return False
        profile = user.profile
        if profile.verified:
            return False
        return True


class IsVerified(permissions.BasePermission):
    """User must be authenticated and flagged as 'verified'"""

    message = "Ce compte n'est pas vérifié"

    def has_permission(self, request, view):
        """Returns True if user is logged in and verified"""
        user = request.user
        if not user.is_authenticated:
            return False
        profile = user.profile
        if not profile.verified:
            return False
        return True
