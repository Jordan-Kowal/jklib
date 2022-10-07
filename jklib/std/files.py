"""Utility functions for managing files and folders."""


# Built-in
import base64
import io
import os
from typing import Union


def convert_size(
    size: Union[int, float], input_units: str = "B", output_units: str = "KB"
) -> float:
    """Converts bytes from one unit to another, rounded up to 2 decimals."""
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    # Errors
    if input_units not in units:
        units_as_text = ", ".join(units)
        raise IndexError(
            "'input_unit' must be one of the following: {}".format(units_as_text)
        )
    if output_units not in units:
        units_as_text = ", ".join(units)
        raise IndexError(
            "'output_unit' must be one of the following: {}".format(units_as_text)
        )
    # Setup
    input_index = units.index(input_units)
    output_index = units.index(output_units)
    n = output_index - input_index
    # Maths
    output_size = round(size / (1024**n), 2)
    return output_size


def create_dirs(*paths: str) -> None:
    """Recursively creates missing folder paths."""
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def decode_file(contents: str) -> io.BytesIO:
    """Decodes raw file contents and returns it."""
    content_type, content_string = contents.split(",")
    return io.BytesIO(base64.b64decode(content_string))


def get_size(path: str, output_units: str = "KB") -> float:
    """Returns the size of a file, in the desired byte unit."""
    byte_size = os.path.getsize(path)
    return convert_size(byte_size, output_units=output_units)
