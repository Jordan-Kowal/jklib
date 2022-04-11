"""Custom managers for Django models"""


# Built-in
from typing import List

# Django
from django.db import models
from django.db.models import Model


class NoBulkCreateManager(models.Manager):
    """Prevents the use of the bulk_create method"""

    def bulk_create(self, objs: List[Model], **kwargs) -> None:
        """Overrides the 'bulk_create' method to make it non-usable"""
        raise NotImplementedError("Cannot use bulk_create on this model")
