# coding: utf-8
"""
Description:
    Contains utility functions for model management
Functions:
    get_object_or_none: Tries to get an object in the database, or returns None
    get_object_or_this: Tries to get an object in the database, or return 'this'
"""


# --------------------------------------------------------------------------------
# > Models
# --------------------------------------------------------------------------------
def get_object_or_none(model, *args, **kwargs):
    """
    Description:
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
        item = None
    return item


def get_object_or_this(model, this=None, *args, **kwargs):
    """
    Description:
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
        obj = this
    return obj
