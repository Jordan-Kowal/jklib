"""Utility functions for maths and working with numbers in general."""

# Built-in
from decimal import Decimal
from typing import Union


def precise_round(value: Union[int, float], points: int) -> Decimal:
    """Improved round() function using the Decimal class."""
    rounded_value = round(value, points)
    precision = f".{'0'*(points-1)}1"
    return Decimal(rounded_value).quantize(Decimal(precision))
