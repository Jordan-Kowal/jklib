from decimal import Decimal
from typing import Union


def precise_round(value: Union[int, float], points: int) -> Decimal:
    """Rounds a number to the given number of decimal points."""
    rounded_value = round(value, points)
    precision = f".{'0'*(points-1)}1"
    return Decimal(rounded_value).quantize(Decimal(precision))
