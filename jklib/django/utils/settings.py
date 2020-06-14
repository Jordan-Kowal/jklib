"""
Contains useful functions for interacting with Django settings
Functions:
    get_config: Tries to get the data from django settings, or returns the default value
"""


# Django
from django.conf import settings


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_config(key, default=None):
    """
    Tries to get the data from django settings, or returns the default value
    Args:
        key (str): The data we are looking for in the settings
        default (*): The default value if the key is not found
    Returns:
        (*) The value found in the settings or the default value
    """
    return getattr(settings, key, default)
