"""DateUpdatedField"""


# Django
from django.db import models


def DateUpdatedField(*args, **kwargs):
    """
    Custom DateTimeField that registers the last update datetime
    Returns:
        (Field) Field instance from Django
    """
    kwargs["auto_now"] = True
    kwargs["verbose_name"] = "Updated at"
    return models.DateTimeField(*args, **kwargs)
