"""Functions for performing SQL queries"""

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
def filter_on_text(queryset, searched_text, min_length, *fields):
    """
    Filters a queryset by searching for a text value in different fields, using OR logic
    :param queryset queryset: A queryset object from a django model which will be our starting point
    :param str searched_text: The text we are looking for
    :param int min_length: The query will execute only if "search_text" length is equal or greater than this
    :param fields: Fields where the text will be searched (SYNTAX: client.name becomes client__name)
    :type fields: list or str
    :return: The filtered and updated queryset
    :rtype: QuerySet
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


def single_sort_by(queryset, sort_by=None, ascending=False):
    """
    Orders and returns the queryset using the GET parameters of a request
    The function takes care of checking if the "sort_by" key exists in the dict
    :param QuerySet queryset: A queryset object from a django model
    :param str sort_by: The field name to sort by
    :param bool ascending: Whether to sort in ascending order
    :return: The sorted and updated queryset
    :rtype: QuerySet
    """
    if sort_by:
        if not ascending:
            sort_by = "-" + sort_by
        queryset = queryset.order_by(sort_by)
    return queryset
