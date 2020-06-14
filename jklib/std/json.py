"""
Contains useful functions for managing JSON files.
Functions:
    sort_json: Overwrites and sorts a JSON file to make it cleaner / more readable
"""


# Built-in
import json
import os


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def sort_json(path):
    """
    Overwrites and sorts a JSON file to make it cleaner / more readable
    Args:
        path (str): Path to the JSON file
    Raises:
        TypeError: The 'path' must lead to a JSON file
    """
    ext = os.path.splitext(path)[1]
    if ext != ".json":
        raise TypeError("The 'path' must lead to a JSON file")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True)
