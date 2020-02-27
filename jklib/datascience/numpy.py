# coding: utf-8
"""
Description:
    Contains useful functions for numpy processing
Functions:
    get_unique_from_numpy: Returns the unique values from a numpy array while keeping its original order
"""


# Third-party
import numpy as np


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_unique_from_numpy(arr):
    """
    Description:
        Returns the unique values from a numpy array while keeping its original order
        (Because numpy.unique automatically re-sort the data)
    Args:
        arr (ndarray): A numpy array
    Returns:
        (list) List of uniques values from the ndarray
    """
    unique_index = np.unique(arr, return_index=True)[1]
    unique_index.sort()
    unique_values = [arr[index] for index in unique_index]
    return unique_values
