"""Functions for interacting with django settings"""


# Django
from django.conf import settings


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_config(key, default=None):
    """
    Tries to get the data from django settings, or returns the default value
    :param key: The data we are looking for in the settings
    :param default: The default value if the key is not found
    :return: The value found in the settings or the default value
    """
    return getattr(settings, key, default)
