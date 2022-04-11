"""Custom fields for Django models"""


# Built-in
from typing import Type, Union

# Django
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    Field,
    ForeignKey,
    Model,
    TextField,
)


def ActiveField(*args, **kwargs) -> BooleanField:
    """Custom BooleanField made for tagging instance as 'active' or 'inactive"""
    kwargs["db_index"] = True
    kwargs["default"] = True
    kwargs["null"] = False
    kwargs["verbose_name"] = "Active"
    return BooleanField(*args, **kwargs)


def CreatedAtField(*args, **kwargs) -> DateTimeField:
    """Custom DateTimeField that registers the creation datetime"""
    kwargs["auto_now_add"] = True
    kwargs["verbose_name"] = "Created at"
    return DateTimeField(*args, **kwargs)


def UpdatedAtField(*args, **kwargs) -> DateTimeField:
    """Custom DateTimeField that registers the last update datetime"""
    kwargs["auto_now"] = True
    kwargs["verbose_name"] = "Updated at"
    return DateTimeField(*args, **kwargs)


def ForeignKeyCascade(to: Union[str, Type[Model]], *args, **kwargs) -> ForeignKey:
    """Custom ForeignKey setup for CASCADE 'on delete' with explicit index"""
    kwargs["db_index"] = True
    kwargs["on_delete"] = CASCADE
    kwargs["null"] = False
    return ForeignKey(to, *args, **kwargs)


def ForeignKeyNull(to: Union[str, Type[Model]], *args, **kwargs) -> ForeignKey:
    """Custom ForeignKey setup for SET_NULL 'on delete' with explicit index"""
    kwargs["db_index"] = True
    kwargs["on_delete"] = SET_NULL
    kwargs["null"] = True
    return ForeignKey(to, *args, **kwargs)


def RequiredField(field: Type[Field], *args, **kwargs) -> Field:
    """Custom CharField that cannot be null nor an empty string"""
    kwargs["blank"] = False
    kwargs["null"] = False
    return field(*args, **kwargs)


class TrimCharField(CharField):
    """CharField with automatic trimming"""

    description: str = (
        "CharField that automatically removes leading and trailing whitespaces"
    )

    def get_prep_value(self, value: str) -> str:
        """Overridden to simply apply trim to the parent method"""
        return super(TrimCharField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance: Model, add: bool) -> str:
        """Overridden to trim the value"""
        return super(TrimCharField, self).pre_save(model_instance, add).strip()


class TrimTextField(TextField):
    """TextField with automatic trimming"""

    description: str = (
        "TextField that automatically removes leading and trailing whitespaces"
    )

    def get_prep_value(self, value: str) -> str:
        """Overridden to simply apply trim to the parent method"""
        return super(TrimTextField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance: Model, add: bool) -> None:
        """Overridden to trim the value"""
        return super(TrimTextField, self).pre_save(model_instance, add).strip()
