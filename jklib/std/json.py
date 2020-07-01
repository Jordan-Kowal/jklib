"""Utility functions for working with JSON files"""


# Built-in
import json
import os


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def sort_json(path):
    """
    Overwrites and sorts a JSON file to make it cleaner / more readable
    :param path: Path to the JSON file
    :raises TypeError: If the given path does not exist
    """
    ext = os.path.splitext(path)[1]
    if ext != ".json":
        raise TypeError("The 'path' must lead to a JSON file")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True)
