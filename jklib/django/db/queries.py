"""
Contains utility functions for making queries in the database
Useful for filtering, sorting, and ordering the data

Simple Getters:
    get_object_or_none: Tries to get an object in the database, or returns None
    get_object_or_this: Tries to get an object in the database, or return 'this'

Advanced Queries:
    filter_on_text: Filters a queryset by searching for a text value in different fields, using OR logic
    single_sort_by: Orders and returns the queryset using the GET parameters of a request
"""


# Django
from django.db.models import Q


# --------------------------------------------------------------------------------
# > Simple Getters
# --------------------------------------------------------------------------------
def get_object_or_none(model, *args, **kwargs):
    """
    Tries to get an object in the database, or returns None
    Args:
        model (Model): The class model from django you want to query
        *args: Args that will be passed to model.objects.get()
        **kwargs: Kwargs that will be passed to model.objects.get()
    Returns:
        (*) A model instance or None
    """
    try:
        item = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    return item


def get_object_or_this(model, this=None, *args, **kwargs):
    """
    Tries to get an object in the database, or return 'this'
    Args:
        model (Model): The class model from django you want to query
        this (*): The alternative value if the object is not found. Defaults to None
        *args: Args that will be passed to model.objects.get()
        **kwargs: Kwargs that will be passed to model.objects.get()
    Returns:
        (*) A model instance or 'this'
    """
    obj = get_object_or_none(model, *args, **kwargs)
    if obj is None:
        return this
    return obj


# --------------------------------------------------------------------------------
# > Advanced Queries
# --------------------------------------------------------------------------------
# TODO: Add a new query that allows for improved list output
#   Filtering:
#       Fieldname + list of exact values (OR)
#       If several filters, relationship of (AND)
#       If same field, overrides
#   Search:
#       Like filtering but: you provide a TEXT and a list of FIELDS that could have it
#       We look for "present in" with OR relationships
#   Sort: Order based on several fields, in given order, [{name: XXX, order: ASC}, ...]
#   Pagination: Quantity of elements, which page number


def filter_on_text(queryset, searched_text, min_length, *fields):
    """
    Filters a queryset by searching for a text value in different fields, using OR logic
    Args:
        queryset (queryset): A queryset object from a django model
        searched_text (str): The text we are looking for
        min_length (int): The query will execute only if "search_text" length is equal or greater than this
        *fields (list of str): Fields where the text will be searched (SYNTAX: client.name becomes client__name)
    Returns:
        (queryset) The filtered and updated queryset
    """
    if len(searched_text) >= min_length:
        q = Q()
        for field in fields:
            key = f"{field}__icontains"
            param = {key: searched_text}
            new_q = Q(**param)
            q |= new_q
        queryset = queryset.filter(q)
    return queryset


def single_sort_by(queryset, params):
    """
    Orders and returns the queryset using the GET parameters of a request
    The function takes care of checking if the "sort_by" key exists in the dict
    Args:
        queryset (queryset): A queryset object from a django model
        params (dict): Dict containing the request params
    Returns:
        (queryset) The sorted and updated queryset
    """
    sort_by = params.get("sort_by", None)
    if sort_by:
        ascending = params.get("ascending", False)
        if ascending != "true":
            sort_by = "-" + sort_by
        queryset = queryset.order_by(sort_by)
    return queryset
