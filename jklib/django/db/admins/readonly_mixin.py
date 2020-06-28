"""ReadOnlyMixin"""

# Local
from .cannot_add_mixin import CannotAddMixin
from .cannot_delete_mixin import CannotDeleteMixin
from .cannot_edit_mixin import CannotEditMixin


class ReadOnlyMixin(CannotAddMixin, CannotDeleteMixin, CannotEditMixin):
    """Admin mixin with read-only permissions"""
