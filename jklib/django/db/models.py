"""Classes and mixins for django models"""


# Django
from django.db.models import Model

# Local
from .fields import CreatedAtField, UpdatedAtField


# --------------------------------------------------------------------------------
# > Models
# --------------------------------------------------------------------------------
class LifeCycleModel(Model):
    """Model that provides lifecycle fields for creation and update"""

    created_at = CreatedAtField()
    updated_at = UpdatedAtField()

    class Meta:
        """Makes the model abstract"""

        abstract = True
