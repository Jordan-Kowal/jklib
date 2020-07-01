"""Scripts and functions related to django security"""


# Django
from django.utils.crypto import get_random_string


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def generate_secret_key():
    """
    Creates a string usable as a "Secret key" using django crypto module
    :return: A randomly generated key
    :rtype: str
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    key = get_random_string(50, chars)
    return key
