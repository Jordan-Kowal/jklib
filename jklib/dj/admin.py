from typing import Optional

from django.db.models import Model
from django.http.request import HttpRequest


class ReadOnlyAdminMixin:
    """Disables all admin actions for a model."""

    @staticmethod
    def has_add_permission(request: HttpRequest, obj: Optional[Model] = None) -> bool:
        return False

    @staticmethod
    def has_delete_permission(
        request: HttpRequest, obj: Optional[Model] = None
    ) -> bool:
        return False

    @staticmethod
    def has_change_permission(
        request: HttpRequest, obj: Optional[Model] = None
    ) -> bool:
        return False
