"""DynamicModelViewSet"""


# Local
from ..mixins import ModelMixin
from .DynamicViewSet import DynamicViewSet


class DynamicModelViewSet(DynamicViewSet, ModelMixin):
    """DynamicViewSet with built-in CRUD actions"""

    pass
