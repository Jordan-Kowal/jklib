# Built-in
from enum import IntEnum
from typing import Any, List, Tuple

# Django
from django.db.models import DateTimeField, Model


class IntChoiceEnum(IntEnum):
    """IntEnum used for a Model choice field"""

    @classmethod
    def choices(cls) -> List[Tuple[int, Any]]:
        return [(key.value, key.name) for key in cls]


class LifeCycleModelMixin(Model):
    """Model mixin that provides lifecycle fields for creation and update"""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

