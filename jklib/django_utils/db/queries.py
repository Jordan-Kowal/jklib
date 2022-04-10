"""Functions for performing SQL queries"""

# Built-in
from typing import Optional, Type

# Django
from django.db.models import Model, Q, QuerySet


def get_object_or_none(model: Type[Model], *args, **kwargs) -> Optional[Model]:
    """Tries to get an object in the database, or returns None"""
    try:
        item = model.objects.get(*args, **kwargs)  # type: ignore
    except model.DoesNotExist:  # type: ignore
        return None
    return item


def filter_on_text(
    queryset: QuerySet, searched_text: str, min_length: int, *fields
) -> QuerySet:
    """Filters a queryset by searching for a text value in different fields, using OR logic"""
    if len(searched_text) >= min_length:
        q = Q()
        for field in fields:
            key = f"{field}__icontains"
            param = {key: searched_text}
            new_q = Q(**param)
            q |= new_q
        queryset = queryset.filter(q)
    return queryset


def single_sort_by(
    queryset: QuerySet, sort_by: str = None, ascending: bool = False
) -> QuerySet:
    """
    Orders and returns the queryset using the GET parameters of a request
    The function takes care of checking if the "sort_by" key exists in the dict
    """
    if sort_by:
        if not ascending:
            sort_by = "-" + sort_by
        queryset = queryset.order_by(sort_by)
    return queryset
