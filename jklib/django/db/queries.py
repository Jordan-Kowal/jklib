"""
Contains utility functions for making queries in the database
Useful for filtering, sorting, and ordering the data
Functions:
    filter_on_text: Filters a queryset by searching for a text value in different fields, using OR logic
    single_sort_by: Orders and returns the queryset using the GET parameters of a request
"""


# Django
from django.db.models import Q


# --------------------------------------------------------------------------------
# > Models
# --------------------------------------------------------------------------------
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
