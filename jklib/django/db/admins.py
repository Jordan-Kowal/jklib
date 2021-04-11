"""Custom classes and mixins for Django admins"""


# --------------------------------------------------------------------------------
# > Simple mixins
# --------------------------------------------------------------------------------
class CannotAddMixin:
    """Prevents user from adding new items through the admin interface"""

    @staticmethod
    def has_add_permission(request):
        """Cannot add new items"""
        return False


class CannotDeleteMixin:
    """Prevents user from deleting items through the admin interface"""

    @staticmethod
    def has_delete_permission(request, obj=None):
        """Cannot delete items"""
        return False


class CannotEditMixin:
    """Prevents user from editing items through the admin interface"""

    @staticmethod
    def has_change_permission(request, obj=None):
        """Cannot update items"""
        return False


class CannotViewMixin:
    """Prevents user from viewing items through the admin interface"""

    @staticmethod
    def has_view_permission(request, obj=None):
        """Cannot delete items"""
        return False


# --------------------------------------------------------------------------------
# > Combo mixins
# --------------------------------------------------------------------------------
class ForbiddenMixin(
    CannotAddMixin, CannotDeleteMixin, CannotEditMixin, CannotViewMixin
):
    """Admin with no CRUD permissions"""


class ReadOnlyMixin(CannotAddMixin, CannotDeleteMixin, CannotEditMixin):
    """Admin with read-only permissions"""
