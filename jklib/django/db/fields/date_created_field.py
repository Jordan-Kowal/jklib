"""DateCreatedField"""


# Django
from django.db import models


def DateCreatedField(*args, **kwargs):
    """
    Custom DateTimeField that registers the creation datetime
    Returns:
        (Field) Field instance from Django
    """
    kwargs["auto_now_add"] = True
    kwargs["verbose_name"] = "Created at"
    return models.DateTimeField(*args, **kwargs)
