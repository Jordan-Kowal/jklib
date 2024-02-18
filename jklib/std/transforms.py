# Built-in
import json
from typing import Any, Dict, List, OrderedDict, Union


def array2d_to_dict(array2d: List[List], col_index: int) -> Dict[Any, List]:
    """Transforms a 2d array into a dict, with one col as key."""
    new_dict = {}
    for row in array2d:
        if isinstance(row, tuple):
            row = list(row)
        key = row.pop(col_index)
        new_dict[key] = row
    return new_dict


def array2d_to_dict_cols(array2d: List[List], cols: List[str]) -> Dict[Any, List]:
    """Creates a dict where the columns are keys.

    Before: [[x1, ..., xn], [y1, ... yn]]
    After: {1: [x1, y1], 2: [x2, y2], ..., n: [xn, yn]}
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
        new_dict[col] = line_sum
        i += 1
    return new_dict


def dict_to_flat_dict(data: Dict[str, Any]) -> Dict[str, Union[str, int, bool]]:
    """Recursively flattens a dict.

    Keys for nested arrays or dicts might look like this:
    'key[0][subkey][3]'
    """
    flat_dict = {}

    def _convert_value(current_path: str, current_value: Any) -> None:
        # Undefined values are skipped
        if current_value is None or current_value == "":
            return
        # Array: Add index to path for each value and recurse
        if type(current_value) == list:  # noqa
            for i, sub_value in enumerate(current_value):
                new_path = f"{current_path}[{i}]"
                _convert_value(new_path, sub_value)
            return
        # Object: Add key to path for each value and recurse
        if type(current_value) == dict:  # noqa
            for sub_key, sub_value in current_value.items():
                new_path = f"{current_path}[{str(sub_key)}]"
                _convert_value(new_path, sub_value)
            return
        # All other cases: Set value
        flat_dict[current_path] = current_value

    for key, value in data.items():
        _convert_value(str(key), value)
    return flat_dict


def ordered_dict_to_dict(ordered_dict: OrderedDict) -> Dict[Any, Any]:
    """Converts an OrderedDict to a dict."""
    return json.loads(json.dumps(ordered_dict))
