"""Utility functions for the numpy library"""


# Third-party
import numpy as np


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_unique_from_numpy(arr):
    """
    Returns the unique values from a numpy array while keeping its original order
    (Because numpy.unique automatically re-sort the data)
    :param ndarray arr: A numpy array
    :return: List of uniques values from the ndarray
    :rtype: list
    """
    unique_index = np.unique(arr, return_index=True)[1]
    unique_index.sort()
    unique_values = [arr[index] for index in unique_index]
    return unique_values
