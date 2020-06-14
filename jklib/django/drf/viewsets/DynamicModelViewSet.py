"""DynamicModelViewSet"""


# Local
from ..mixins import ModelMixin
from .DynamicViewSet import DynamicViewSet


class DynamicModelViewSet(DynamicViewSet, ModelMixin):
    """Dynamic viewset for Django models which includes the basic CRUD"""

    pass
