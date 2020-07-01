"""Utility functions for transforming/converting objects into other shapes/things"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def array2d_to_dict(array2d, pk):
    """
    Transforms a 2d array into a dict, with one of the fields as primary key
    :param array2d: Any 2d list
    :type array2d: list(list)
    :param int pk: The column index to use as a key
    :return: Dict of lists, with keys being the values from the initial "pk" column
    :rtype: dict(list)
    """
    new_dict = {}
    for row in array2d:
        if isinstance(row, tuple):
            row = list(row)
        key = row.pop(pk)
        new_dict[key] = row
    return new_dict


def array2d_to_dict_cols(array2d, cols):
    """
    Creates a dict where each key holds a list that contains 1 value from each list
    Before: [[x1, ..., xn], [y1, ... yn]]
    After: {1: [x1, y1], 2: [x2, y2]}
    :param array2d: List of lists where each sublist should be of similar length
    :type array2d: list(list)
    :param cols: List of column names. Should be the same length as the nested lists
    :type cols: list(str)
    :return: Dict of lists with "cols" as keys, with values from each nested list
    :rtype: dict(list)
    """
    for line in array2d:
        if len(line) != len(cols):
            raise TypeError("Both lists must contain the same number of elements")
    new_dict = {}
    i = 0
    for col in cols:
        line_sum = []
        for line in array2d:
            line_sum.append(line[i])
        i += 1
        new_dict[col] = line_sum
    return new_dict
