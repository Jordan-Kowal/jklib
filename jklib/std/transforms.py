"""
Functions to transform objects into other shapes
Functions:
    array2d_to_dict: Transforms a 2d array into a dict, with one of the fields as primary key
    array2d_to_dict_cols: Creates a dict where each key holds a list that contains 1 value from each list
"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def array2d_to_dict(array, pk):
    """
    Transforms a 2d array into a dict, with one of the fields as primary key
    Args:
        array (list): List of lists
        pk (int): The column index to use as a key
    Returns:
        (dict) Dict of lists, with keys being the values from the initial "pk" column
    """
    new_dict = {}
    for row in array:
        if isinstance(row, tuple):
            row = list(row)
        key = row.pop(pk)
        new_dict[key] = row
    return new_dict


def array2d_to_dict_cols(array, cols):
    """
    Creates a dict where each key holds a list that contains 1 value from each list
    Before: [[x1, ..., xn], [y1, ... yn]]
    After: {1: [x1, y1], 2: [x2, y2]}
    Args:
        array (list): List of lists. Each sublist should be of similar length
        cols (list): List of column names. Should be the same length as the nested lists
    Returns:
        (dict) Dict of lists with "cols" as keys, with values from each nested list
    """
    for line in array:
        if len(line) != len(cols):
            raise TypeError("Both lists must contain the same number of elements")
    new_dict = {}
    i = 0
    for col in cols:
        line_sum = []
        for line in array:
            line_sum.append(line[i])
        i += 1
        new_dict[col] = line_sum
    return new_dict
