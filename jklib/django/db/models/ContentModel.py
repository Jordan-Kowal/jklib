"""ContentModel"""


# Django
from django.db import models

# Local
from ..fields import ActiveField, DateCreatedField, DateUpdatedField


class ContentModel(models.Model):
    """
    Abstract model for 'Content tables' that adds 3 new fields
    A 'Content model' is a model that stores content, as opposed to lookup tables
    The 3 new fields are: active, date_create, and date_updated
    """

    # ----------------------------------------
    # Fields
    # ----------------------------------------
    active = ActiveField()
    created_at = DateCreatedField()
    updated_at = DateUpdatedField()

    # ----------------------------------------
    # META, str, save, get_absolute_url
    # ----------------------------------------
    class Meta:
        """Metadata to configure our model in the database"""

        abstract = True
