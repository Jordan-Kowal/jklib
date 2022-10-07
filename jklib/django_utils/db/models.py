# Django
from django.db.models import DateTimeField, Model


class LifeCycleModelMixin(Model):
    """Model mixin that provides lifecycle fields for creation and update."""

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
