"""BlockAll"""


# Django
from rest_framework import permissions


class BlockAll(permissions.BasePermission):
    """Blocks all incoming traffic"""

    message = "Access restricted"

    def has_permission(self, request, view):
        """Always denied"""
        return False

    def has_object_permission(self, request, view, obj):
        """Always denied"""
        return False
