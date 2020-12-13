"""
Custom fields for django models
Split in the following categories:
    Shortcuts:      Function-based fields that simply defaults various kwargs for Django fields
    Custom Fields:  Actual class-based fields for our custom needs
"""


# Django
from django.db import models


# --------------------------------------------------------------------------------
# > Shortcuts
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


# --------------------------------------------------------------------------------
# > Custom Fields
# --------------------------------------------------------------------------------
class TrimCharField(models.CharField):
    """CharField with automatic trimming"""

    description = (
        "CharField that automatically removes leading and trailing whitespaces"
    )

    def get_prep_value(self, value):
        """
        Overridden to simply apply trim to the parent method
        :param str value: Value of the field
        :return: The trimmed value
        :rtype: str
        """
        return super(TrimCharField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance, add):
        """
        :param Model model_instance: The model instance where our field is
        :param bool add: Whether the instance does not yet exist in the database
        :return: The trimmed value
        :rtype: str
        """
        return super(TrimCharField, self).pre_save(model_instance, add).strip()


class TrimTextField(models.TextField):
    """TextField with automatic trimming"""

    description = (
        "TextField that automatically removes leading and trailing whitespaces"
    )

    def get_prep_value(self, value):
        """
        Overridden to simply apply trim to the parent method
        :param str value: Value of the field
        :return: The trimmed value
        :rtype: str
        """
        return super(TrimTextField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance, add):
        """
        :param Model model_instance: The model instance where our field is
        :param bool add: Whether the instance does not yet exist in the database
        :return: The trimmed value
        :rtype: str
        """
        return super(TrimTextField, self).pre_save(model_instance, add).strip()
