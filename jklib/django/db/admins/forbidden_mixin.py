"""ReadOnlyMixin"""


# Local
from .cannot_add_mixin import CannotAddMixin
from .cannot_delete_mixin import CannotDeleteMixin
from .cannot_edit_mixin import CannotEditMixin
from .cannot_view_mixin import CannotViewMixin


class ForbiddenMixin(
    CannotAddMixin, CannotDeleteMixin, CannotEditMixin, CannotViewMixin
):
    """Admin mixin with no CRUD permissions"""
