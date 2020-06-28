"""ActiveField"""


# Django
from django.db import models


def ActiveField(*args, **kwargs):
    """
    Custom BooleanField made for tagging instance as 'active' or 'inactive
    Returns:
        (Field) Field instance from Django
    """
    kwargs["db_index"] = True
    kwargs["default"] = True
    kwargs["null"] = False
    kwargs["verbose_name"] = "Active"
    return models.BooleanField(*args, **kwargs)
