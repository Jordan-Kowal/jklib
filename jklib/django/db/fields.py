"""
Custom fields for django models
We use instances instead of classes so that django can detect changes and automatically build migrations
"""


# Django
from django.db import models


# --------------------------------------------------------------------------------
# > Fields
# --------------------------------------------------------------------------------
def ActiveField(*args, **kwargs):
    """
    Custom BooleanField made for tagging instance as 'active' or 'inactive
    :param args: Same args as the django Field class
    :param kwargs: Same kwargs as the django Field class
    :return: Instance from the django Field model
    :rtype: Field
    """
    kwargs["db_index"] = True
    kwargs["default"] = True
    kwargs["null"] = False
    kwargs["verbose_name"] = "Active"
    return models.BooleanField(*args, **kwargs)


def DateCreatedField(*args, **kwargs):
    """
    Custom DateTimeField that registers the creation datetime
    :param args: Same args as the django Field class
    :param kwargs: Same kwargs as the django Field class
    :return: Instance from the django Field model
    :rtype: Field
    """
    kwargs["auto_now_add"] = True
    kwargs["verbose_name"] = "Created at"
    return models.DateTimeField(*args, **kwargs)


def DateUpdatedField(*args, **kwargs):
    """
    Custom DateTimeField that registers the last update datetime
    :param args: Same args as the django Field class
    :param kwargs: Same kwargs as the django Field class
    :return: Instance from the django Field model
    :rtype: Field
    """
    kwargs["auto_now"] = True
    kwargs["verbose_name"] = "Updated at"
    return models.DateTimeField(*args, **kwargs)


def ForeignKeyCascade(to, *args, **kwargs):
    """
    Custom ForeignKey setup for CASCADE 'on delete' with explicit index
    :param to: The target model for the foreign key relation
    :type to: str or Model
    :param args: Same args as the django Field class
    :param kwargs: Same kwargs as the django Field class
    :return: Instance from the django Field model
    :rtype: Field
    """
    kwargs["db_index"] = True
    kwargs["on_delete"] = models.CASCADE
    kwargs["null"] = False
    return models.ForeignKey(to, *args, **kwargs)


def ForeignKeyNull(to, *args, **kwargs):
    """
    Custom ForeignKey setup for SET_NULL 'on delete' with explicit index
    :param to: The target model for the foreign key relation
    :type to: str or Model
    :param args: Same args as the django Field class
    :param kwargs: Same kwargs as the django Field class
    :return: Instance from the django Field model
    :rtype: Field
    """
    kwargs["db_index"] = True
    kwargs["on_delete"] = models.SET_NULL
    kwargs["null"] = True
    return models.ForeignKey(to, *args, **kwargs)


def RequiredField(field, *args, **kwargs):
    """
    Custom CharField that cannot be null nor an empty string
    :param Field field: Field class from Django
    :param args: Same args as the django Field class
    :param kwargs: Same kwargs as the django Field class
    :return: Instance from the django Field model
    :rtype: Field
    """
    kwargs["blank"] = False
    kwargs["null"] = False
    return field(*args, **kwargs)
