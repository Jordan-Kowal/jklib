"""Functions for interacting with django settings."""

# Built-in
from typing import Any

# Django
from django.conf import settings


def get_config(key: str, default: Any = None) -> Any:
    """Tries to get the data from django settings, or returns the default
    value."""
    return getattr(settings, key, default)
