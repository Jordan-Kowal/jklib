# coding: utf-8
"""
Description:
    Utility functions related to maths
Functions:
    precise_round: Improved round() function
"""


# Built-in
from decimal import Decimal


# ---------------------------------------- ----------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def precise_round(value, points: int):
    """
    Description:
        Improved round() function
        Using the Decimal module, we get rid of the infinite floating point caused by round()
    Args:
        value (int, float): the value the round
        points (int): the number of decimals you want
    """
    pass
    rounded_value = round(value, points)
    precision = f".{'0'*(points-1)}1"
    return Decimal(rounded_value).quantize(Decimal(precision))
