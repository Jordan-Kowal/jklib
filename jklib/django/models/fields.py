# coding: utf-8
"""
Contains functions to generate preset different type of Field
We use functions instead of classes so that Django can detect our changes
Fields:
    ActiveField: BooleanField made for tagging instance as 'active' or 'inactive'
    DateCreatedField: DateTimeField that registers the creation datetime
    DateUpdatedField: DateTimeField that registers the last update datetime
    ForeignKeyCascade: ForeignKey set up for CASCADE 'on delete' with index
    ForeignKeyNull: ForeignKey set up for SET_NULL 'on delete' with index
    NotEmptyCharField: CharField that cannot be null nor an empty string
"""


# Django
from django.db import models


# --------------------------------------------------------------------------------
# > Fields
# --------------------------------------------------------------------------------
def ActiveField(*args, **kwargs):
    """
    Custom BooleanField made for tagging instance as 'active' or 'inactive
    Returns:
        (Field) Field instance from Django
    """
    kwargs["db_index"] = True
    kwargs["default"] = True
    kwargs["null"] = False
    kwargs["verbose_name"] = "Actif"
    return models.BooleanField(*args, **kwargs)


def DateCreatedField(*args, **kwargs):
    """
    Custom DateTimeField that registers the creation datetime
    Returns:
        (Field) Field instance from Django
    """
    kwargs["auto_now_add"] = True
    kwargs["verbose_name"] = "Créé(e) le"
    return models.DateTimeField(*args, **kwargs)


def DateUpdatedField(*args, **kwargs):
    """
    Custom DateTimeField that registers the last update datetime
    Returns:
        (Field) Field instance from Django
    """
    kwargs["auto_now"] = True
    kwargs["verbose_name"] = "Mis(e) à jour le"
    return models.DateTimeField(*args, **kwargs)


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


def NotEmptyCharField(*args, **kwargs):
    """
    Custom Charfield that cannot be null nor an empty string
    Returns:
        (Field) Field instance from Django
    """
    kwargs["blank"] = False
    kwargs["null"] = False
    return models.CharField(*args, **kwargs)
