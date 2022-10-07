"""Functions for performing SQL queries."""

# Built-in
from typing import Any, List, Optional, Type

# Django
from django.db.models import Manager, Model


def maybe_get_instance(
    model_class: Type[Model], *args: Any, **kwargs: Any
) -> Optional[Model]:
    """Tries to get an object in the database or returns None."""
    try:
        item = model_class.objects.get(*args, **kwargs)
    except model_class.DoesNotExist:
        return None
    return item


def update_model(instance: Model, **kwargs: Any) -> Model:
    """Updates multiple fields of a model instance and saves it."""
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
