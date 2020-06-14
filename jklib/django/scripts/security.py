"""
Useful scripts for Django
Functions:
    generate_secret_key: Creates a string usable as a "Secret key" using django crypto module
"""


# Django
from django.utils.crypto import get_random_string


# --------------------------------------------------------------------------------
# > Script
# --------------------------------------------------------------------------------
def generate_secret_key():
    """
    Creates a string usable as a "Secret key" using django crypto module
    Returns:
        (str) A randomly generated key
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    key = get_random_string(50, chars)
    return key
