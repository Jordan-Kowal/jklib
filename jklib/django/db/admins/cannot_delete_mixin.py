"""CannotDeleteMixin"""


class CannotDeleteMixin:
    """Admin mixin to prevent user from deleting items through the admin interface"""

    @staticmethod
    def has_delete_permission(request, obj=None):
        """Cannot delete items"""
        return False
