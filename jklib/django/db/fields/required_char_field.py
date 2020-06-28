"""NotEmptyCharField"""


# Django
from django.db import models


def RequiredCharField(*args, **kwargs):
    """
    Custom Charfield that cannot be null nor an empty string
    Returns:
        (Field) Field instance from Django
    """
    kwargs["blank"] = False
    kwargs["null"] = False
    return models.CharField(*args, **kwargs)
