"""IsVerified"""


# Django
from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    """User must be authenticated and flagged as 'verified'"""

    message = "You must have a verified account"

    def has_permission(self, request, view):
        """Returns True if user is logged in and verified"""
        user = request.user
        if not user.is_authenticated:
            return False
        profile = user.profile
        if not profile.is_verified:
            return False
        return True
