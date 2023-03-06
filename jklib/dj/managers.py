# Built-in
from typing import Iterable, List, Optional, Sequence

# Django
from django.db import models


class NoBulkManager(models.Manager):
    """Disables bulk operations on a model."""

    def bulk_create(
        self,
        objs: Iterable,
        batch_size: Optional[int] = ...,
        ignore_conflicts: bool = ...,
    ) -> List:
        raise NotImplementedError

    def bulk_update(
        self, objs: Iterable, fields: Sequence[str], batch_size: Optional[int] = ...
    ) -> int:
        raise NotImplementedError
