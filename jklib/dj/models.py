# Built-in
import os
import uuid
from typing import Any, List, Optional, Type

# Django
from django import forms
from django.db import IntegrityError
from django.db.models import DateTimeField, Manager, Model
from django.utils.deconstruct import deconstructible


class LifeCycleAbstractModel(Model):
    """Model that adds created_at and updated_at fields."""

    created_at = DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True


class PreCleanedAbstractModel(Model):
    """Model that calls .full_clean() before saving."""

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        self._perform_pre_save_clean()
        super().save(*args, **kwargs)

    def _perform_pre_save_clean(self) -> None:
        """Calls .full_clean() and changes ValidationErrors to
        IntegrityErrors."""
        try:
            self.full_clean()
        except forms.ValidationError as e:
            raise IntegrityError(e)
        except Exception as e:
            raise e


@deconstructible
class FileNameWithUUID(object):
    """Generates a unique file name with a UUID."""

    def __init__(self, path: str) -> None:
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _: Any, filename: str) -> str:
        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return self.path % (name + "_" + str(uuid.uuid4()), extension)


def maybe_get_instance(
    model_class: Type[Model], *args: Any, **kwargs: Any
) -> Optional[Model]:
    """Returns an instance of a model if it exists, otherwise returns None."""
    try:
        item = model_class.objects.get(*args, **kwargs)
    except model_class.DoesNotExist:
        return None
    return item


def update_model_instance(instance: Model, **kwargs: Any) -> Model:
    """Updates a model instance with the provided kwargs."""
    for key, value in kwargs.items():
        setattr(instance, key, value)
    instance.save()
    return instance


def update_m2m(
    m2m_field: Manager,
    ids: List[str],
) -> None:
    """Updates a many-to-many field with a list of ids."""
    unique_ids = set(ids or [])
    existing_m2m_fks = m2m_field.all().values_list("id", flat=True)
    # Delete m2m instances that are not in the provided ids
    m2m_fks_to_delete = [id_ for id_ in existing_m2m_fks if id_ not in unique_ids]
    if len(m2m_fks_to_delete) > 0:
        m2m_field.remove(*m2m_fks_to_delete)
    # Create m2m instances that are not in the existing instances
    fks_to_add = [id_ for id_ in unique_ids if id_ not in existing_m2m_fks]
    if len(fks_to_add) > 0:
        m2m_field.add(*fks_to_add)
