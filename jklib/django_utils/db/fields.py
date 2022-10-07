"""Custom fields for Django models."""
# Built-in
import os
import uuid
from typing import Any

# Django
from django.db.models import CharField, Model, TextField
from django.utils.deconstruct import deconstructible


class TrimCharField(CharField):
    """CharField with automatic trimming."""

    description: str = (
        "CharField that automatically removes leading and trailing whitespaces"
    )

    def get_prep_value(self, value: str) -> str:
        """Overridden to simply apply trim to the parent method."""
        return super(TrimCharField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance: Model, add: bool) -> str:
        """Overridden to trim the value."""
        return super(TrimCharField, self).pre_save(model_instance, add).strip()


class TrimTextField(TextField):
    """TextField with automatic trimming."""

    description: str = (
        "TextField that automatically removes leading and trailing whitespaces"
    )

    def get_prep_value(self, value: str) -> str:
        """Overridden to simply apply trim to the parent method."""
        return super(TrimTextField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance: Model, add: bool) -> None:
        """Overridden to trim the value."""
        return super(TrimTextField, self).pre_save(model_instance, add).strip()


@deconstructible
class FileNameWithUUID(object):
    """When given to a FileField or ImageField in the upload_to argument, it
    will add an uuid to the filename to avoid name collisions.

    Example: FileNameWithUUID("path/to/directory/")
    """

    def __init__(self, path: str) -> None:
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _: Any, filename: str) -> str:
        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return self.path % (name + "_" + str(uuid.uuid4()), extension)
