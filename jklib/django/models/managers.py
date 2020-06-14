# coding: utf-8
"""
Contains useful function for managing models.
Managers:
    NoBulkManager: Prevents the use of the bulk_create method
"""


# Django
from django.db import models


# --------------------------------------------------------------------------------
# > Managers
# --------------------------------------------------------------------------------
class NoBulkCreateManager(models.Manager):
    """Prevents the use of the bulk_create method"""

    def bulk_create(self, objs, **kwargs):
        """Not implemented"""
        raise NotImplementedError("Cannot use bulk_create on this model")
