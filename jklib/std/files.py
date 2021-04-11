"""Utility functions for managing files and folders"""


# Built-in
import base64
import io
import os


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def convert_size(size, input_units="B", output_units="KB"):
    """
    Converts bytes from one unit to another, rounded up to 2 decimals
    :param size: The initial amount of bytes
    :type size: int or float
    :param str input_units: The current unit for the given amount. Defaults to "B".
    :param str output_units: The desired unit to convert to. Defaults to "KB".
    :return: The converted amount of bytes, in the desired unit, rounded to 2 digits
    :rtype: float
    :raise IndexError: if 'input_unit' or 'output_units' are not in the valid unit list
    """
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
    output_size = round(size / (1024 ** n), 2)
    return output_size


def create_dirs(*paths):
    """
    For each given folder path, check if it exists. If not, it will create it
    :param str paths: Paths to the folder
    """
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def decode_file(contents):
    """
    Decodes raw file contents and returns it
    :param str contents: File content
    :return: The decoded content
    :rtype: str
    """
    content_type, content_string = contents.split(",")
    decoded = io.BytesIO(base64.b64decode(content_string))
    return decoded


def get_size(path, output_units="KB"):
    """
    Returns the size of a file, in the desired byte unit
    :param path: Path to the file
    :param output_units: The desired byte unit. Defaults to "KB".
    :return: The file size in the requested byte unit
    :rtype: float
    """
    byte_size = os.path.getsize(path)
    size = convert_size(byte_size, output_units=output_units)
    return size
