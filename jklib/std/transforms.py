"""Utility functions for transforming/converting objects into other
shapes/things."""
# Built-in
from typing import Any, Dict, List


def array2d_to_dict(array2d: List[List], pk: int) -> Dict[Any, List]:
    """Transforms a 2d array into a dict, with one of the fields as primary
    key."""
    new_dict = {}
    for row in array2d:
        if isinstance(row, tuple):
            row = list(row)
        key = row.pop(pk)
        new_dict[key] = row
    return new_dict


def array2d_to_dict_cols(array2d: List[List], cols: List[str]) -> Dict[Any, List]:
    """
    Creates a dict where each key holds a list that contains 1 value from each list
    Before: [[x1, ..., xn], [y1, ... yn]]
    After: {1: [x1, y1], 2: [x2, y2]}
    """
    for line in array2d:
        if len(line) != len(cols):
            raise ValueError("Both lists must contain the same number of elements")
    new_dict = {}
    i = 0
    for col in cols:
        line_sum = []
        for line in array2d:
            line_sum.append(line[i])
        i += 1
        new_dict[col] = line_sum
    return new_dict
