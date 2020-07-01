"""Utility functions for maths and working with numbers in general"""


# Built-in
from decimal import Decimal


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def precise_round(value, points: int):
    """
    Improved round() function using the Decimal class
    :param value: The value the round
    :type value: int or float
    :param int points: The number of decimals you want
    :return: The rounded value as a Decimal instance
    :rtype: Decimal
    """
    pass
    rounded_value = round(value, points)
    precision = f".{'0'*(points-1)}1"
    return Decimal(rounded_value).quantize(Decimal(precision))
