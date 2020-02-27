# coding: utf-8
"""
Description:
    Contains useful function for managing files and folders.
Functions:
    convert_size: Converts bytes from one unit to another, rounded up to 2 decimals
    create_dirs: For each given folder path, check if it exists. If not, it will create it
    decode_file: Decodes raw file contents and returns it
    get_size: Returns the size of a file, in the desired byte unit
"""


# Built-in
import base64
import io
import os


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def convert_size(size, input_unit="B", output_unit="KB"):
    """
    Description:
        Converts bytes from one unit to another, rounded up to 2 decimals
    Args:
        size (int/float): The initial amount of bytes
        input_unit (str, optional): The current unit for the given amount. Defaults to "B".
        output_unit (str, optional): The desired unit to convert to. Defaults to "KB".
    Raises:
        IndexError: 'input_unit' must be one in 'units'
        IndexError: 'output_unit' must be one in 'units'
    Returns:
        float: The converted amount of bytes, in the desired unit, rounded to 2 digits
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    # Errors
    if input_unit not in units:
        units_as_text = ", ".join(units)
        raise IndexError(
            "'input_unit' must be one of the following: {}".format(units_as_text)
        )
    if output_unit not in units:
        units_as_text = ", ".join(units)
        raise IndexError(
            "'output_unit' must be one of the following: {}".format(units_as_text)
        )
    # Setup
    input_index = units.index(input_unit)
    output_index = units.index(output_unit)
    n = output_index - input_index
    # Maths
    output_size = round(size / (1024 ** n), 2)
    return output_size


def create_dirs(*paths):
    """
    Description:
        For each given folder path, check if it exists. If not, it will create it
    Args:
        *paths (str): Paths to the folder
    """
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def decode_file(contents):
    """Decodes raw file contents and returns it"""
    content_type, content_string = contents.split(",")
    decoded = io.BytesIO(base64.b64decode(content_string))
    return decoded


def get_size(path, unit="KB"):
    """
    Description:
        Returns the size of a file, in the desired byte unit
    Args:
        path (str): Path to the file
        unit (str, optional): The desired byte unit. Defaults to "KB".
    Returns:
        float: The file size in the requested byte unit
    """
    byte_size = os.path.getsize(path)
    size = convert_size(byte_size)
    return size
