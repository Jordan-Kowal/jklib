"""IsObjectOwner"""


# Django
from rest_framework import permissions


class IsObjectOwner(permissions.BasePermission):
    """Object must be attached to the user, or be the user itself"""

    message = "Access restricted"

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
