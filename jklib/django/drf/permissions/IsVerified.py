"""IsVerified"""


# Django
from rest_framework import permissions


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
