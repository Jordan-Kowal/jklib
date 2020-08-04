"""
Permission classes that aim to ENTIRELY replace the DRF permissions.

When checking permissions, DRF will natively:
    Check 'has_permission' for each class
    Then, if it is related to an object, check 'has_object_permission'
However, because both methods default to True, this can lead to some unexpected behavior.
Implementing a permission with only "has_object_permission" means that it will always access non-detail actions

We made the following changes to the workflow:
    Created a new 'ImprovedBasePermission' class and rebuilt all DRF classes from it
    'has_object_permission' will default to 'has_permission'
    'detail_only' has been added to flag a permission has "only usable in detailed actions"
    Our DynamicViewSet adds the 'detail' information into the request before the permission check
"""


# Django
from rest_framework.permissions import BasePermission


# --------------------------------------------------------------------------------
# > Meta
# --------------------------------------------------------------------------------
class ImprovedBasePermission(BasePermission):
    """
    Improved version of the DRF BasePermission class:
        'detail_only' can be used to limit a permission to detail views
        The default 'has_permission' checks the 'detail_only' requirement for permissions
        The default 'has_object_permission' falls back on 'has_permission' if not explicitly implemented
    """

    detail_only = False

    def has_permission(self, request, view):
        """True by default, except for detail-only permissions when the action is not detail"""
        if self.detail_only:
            return request.is_detail_action  # Added in viewset.check_permissions
        else:
            return True

    def has_object_permission(self, request, view, obj):
        """Falls back to the 'has_permission' method"""
        return self.has_permission(request, view)


# --------------------------------------------------------------------------------
# > DRF Permissions
# --------------------------------------------------------------------------------
class AllowAny(ImprovedBasePermission):
    """Allows anyone"""

    pass


class IsAuthenticated(ImprovedBasePermission):
    """User needs to be authenticated"""

    @staticmethod
    def has_permission(request, view):
        """Returns True if the user is logged in"""
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(ImprovedBasePermission):
    """Allows access only to admin users"""

    @staticmethod
    def has_permission(request, view):
        """Returns True if user is admin"""
        return bool(request.user and request.user.is_staff)


# --------------------------------------------------------------------------------
# > Custom Permissions
# --------------------------------------------------------------------------------
class BlockAll(ImprovedBasePermission):
    """Blocks all incoming traffic. Equivalent to ~AllowAny, but makes it explicit"""

    message = "Access denied"

    @staticmethod
    def has_permission(request, view):
        """Always denied"""
        return False


class IsNotAuthenticated(ImprovedBasePermission):
    """User must be disconnected. Equivalent to ~IsAuthenticated, but makes it explicit"""

    message = "You must logout to access this service"

    @staticmethod
    def has_permission(request, view):
        """Returns true if user is not logged in"""
        return not bool(request.user and request.user.is_authenticated)


class IsNotVerified(ImprovedBasePermission):
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


class IsObjectOwner(ImprovedBasePermission):
    """Object must be attached to the user, or be the user itself"""

    detail_only = True
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


class IsSuperUser(ImprovedBasePermission):
    """Allows access only to superusers"""

    def has_permission(self, request, view):
        """Returns whether the user is a superuser"""
        return bool(request.user and request.user.is_superuser)


class IsVerified(ImprovedBasePermission):
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
