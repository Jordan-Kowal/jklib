"""DynamicModelViewSet"""


# Local
from ..mixins import ModelMixin
from .dynamic_viewset import DynamicViewSet


class DynamicModelViewSet(DynamicViewSet, ModelMixin):
    """DynamicViewSet with built-in CRUD actions"""

    pass
