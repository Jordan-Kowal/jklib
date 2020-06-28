"""ForeignKeyCascade"""


# Django
from django.db import models


def ForeignKeyCascade(to, *args, **kwargs):
    """
    Custom ForeignKey set up for CASCADE 'on delete' with index
    Args:
        to (string|Model): The target model for the foreign key relation
    Returns:
        (Field) Field instance from Django
    """
    kwargs["db_index"] = True
    kwargs["on_delete"] = models.CASCADE
    kwargs["null"] = False
    return models.ForeignKey(to, *args, **kwargs)
