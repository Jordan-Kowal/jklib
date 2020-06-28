"""CannotAddMixin"""


class CannotAddMixin:
    """Admin mixin to prevent user from adding new items through the admin interface"""

    @staticmethod
    def has_add_permission(request):
        """Cannot add new items"""
        return False
