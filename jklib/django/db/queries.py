"""
Contains utility functions for making queries in the database
Useful for filtering, sorting, and ordering the data

Split into sub-categories:
    Simple Getters: Shortcut to get an object
    Advanced Queries: Getters with several parameters and improved searches
"""


# Django
from django.db.models import Q


# --------------------------------------------------------------------------------
# > Simple Getters
# --------------------------------------------------------------------------------
def get_object_or_none(model, *args, **kwargs):
    """
    Tries to get an object in the database, or returns None
    :param Model model: The class model from django you want to query
    :param args: Args that will be passed to model.objects.get()
    :param kwargs: Kwargs that will be passed to model.objects.get()
    :return: Either the model instance or None
    :rtype: Model or None
    """
    try:
        item = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    return item


def get_object_or_this(model, default=None, *args, **kwargs):
    """
    Tries to get an object in the database, or return 'this'
    :param Model model: The class model from django you want to query
    :param default: The value returned if the model is not found
    :param args: Args that will be passed to model.objects.get()
    :param kwargs: Kwargs that will be passed to model.objects.get()
    :return: Either the model instance or the default value
    :rtype: Model or *
    """
    obj = get_object_or_none(model, *args, **kwargs)
    if obj is None:
        return default
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
    :param queryset queryset: A queryset object from a django model which will be our starting point
    :param str searched_text: The text we are looking for
    :param int min_length: The query will execute only if "search_text" length is equal or greater than this
    :param fields: Fields where the text will be searched (SYNTAX: client.name becomes client__name)
    :type fields: list or str
    :return: The filtered and updated queryset
    :rtype: queryset
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
    :param queryset queryset: A queryset object from a django model
    :param dict params: Dict containing the request params
    :return: The sorted and updated queryset
    :rtype: queryset
    """
    sort_by = params.get("sort_by", None)
    if sort_by:
        ascending = params.get("ascending", False)
        if ascending != "true":
            sort_by = "-" + sort_by
        queryset = queryset.order_by(sort_by)
    return queryset
