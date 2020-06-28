"""CannotViewMixin"""


class CannotViewMixin:
    """Admin mixin to prevent user from viewing items through the admin interface"""

    @staticmethod
    def has_view_permission(request, obj=None):
        """Cannot delete items"""
        return False
