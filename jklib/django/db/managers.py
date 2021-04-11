"""Custom managers for Django models"""


# Django
from django.db import models


# --------------------------------------------------------------------------------
# > Managers
# --------------------------------------------------------------------------------
class NoBulkCreateManager(models.Manager):
    """Prevents the use of the bulk_create method"""

    def bulk_create(self, objs, **kwargs):
        """
        Overrides the 'bulk_create' method to make it non-usable
        :raise NotImplementedError: Must be overridden to be usable
        """
        raise NotImplementedError("Cannot use bulk_create on this model")
