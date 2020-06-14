"""IsNotAuthenticated"""


# Django
from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """User must be disconnected"""

    message = "You must logout"

    def has_permission(self, request, view):
        """Returns true if user is not logged in"""
        authenticated = request.user.is_authenticated
        return not authenticated
