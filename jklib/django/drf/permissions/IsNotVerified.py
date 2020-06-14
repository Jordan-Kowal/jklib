"""IsNotVerified"""


# Django
from rest_framework import permissions


class IsNotVerified(permissions.BasePermission):
    """User must be authenticated but not yet verified"""

    message = "Your account must not be verified"

    def has_permission(self, request, view):
        """Returns True if user is logged in and not verified"""
        user = request.user
        if not user.is_authenticated:
            return False
        profile = user.profile
        if profile.verified:
            return False
        return True
