"""Utility functions for the numpy library."""

# Built-in
from typing import Any, List

# Third-party
import numpy as np


def get_unique_from_numpy(arr: np.ndarray) -> List[Any]:
    """Returns the unique values from a numpy array while keeping its original
    order."""
    unique_index = np.unique(arr, return_index=True)[1]
    unique_index.sort()
    unique_values = [arr[index] for index in unique_index]
    return unique_values
