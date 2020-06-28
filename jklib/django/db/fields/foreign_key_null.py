"""ForeignKeyNull"""


# Django
from django.db import models


def ForeignKeyNull(to, *args, **kwargs):
    """
    Custom ForeignKey set up for SET_NULL 'on delete' with index
    Returns:
        (Field) Field instance from Django
    """
    kwargs["db_index"] = True
    kwargs["on_delete"] = models.SET_NULL
    kwargs["null"] = True
    return models.ForeignKey(to, *args, **kwargs)
