"""Model classes and mixins for Django"""


# Local
from ..fields import DateCreatedField, DateUpdatedField


class LifeCycleMixin:
    """Model mixin that provides lifecycle fields for creation and update"""

    # ----------------------------------------
    # Fields
    # ----------------------------------------
    created_at = DateCreatedField()
    updated_at = DateUpdatedField()
