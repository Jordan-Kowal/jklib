"""Utility function for classes in general."""
# Built-in
from typing import Any, Type


def is_subclass(obj: Any, reference_class: Type[Any]) -> bool:
    """Improvement of 'issubclass' that returns False if the first arg is not
    an actual class."""
    try:
        return issubclass(obj, reference_class)
    except TypeError:
        return False
