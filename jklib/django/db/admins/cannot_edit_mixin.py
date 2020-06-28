"""CannotEditMixin"""


class CannotEditMixin:
    """Admin mixin to prevent user from editing items through the admin interface"""

    @staticmethod
    def has_change_permission(request, obj=None):
        """Cannot update items"""
        return False
