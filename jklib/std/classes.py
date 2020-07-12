"""Utility function for classes in general"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def is_subclass(obj, reference_class):
    """
    Improvement of 'issubclass' that returns False if the first arg is not an actual class
    :param obj: The object you want information on
    :param reference_class: The reference class to compare to
    :return: Whether 'obj' inherits from 'reference_class'
    :rtype: bool
    """
    try:
        return issubclass(obj, reference_class)
    except TypeError:
        return False
