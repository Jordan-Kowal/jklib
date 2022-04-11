"""Functions for managing image files, mostly through the pillow/PIL library"""

# Built-in
from typing import Tuple, Union

# Django
from django.utils.safestring import mark_safe

# Third-party
from PIL import Image


def downsize_image(file_path: str, width: int, height: int) -> None:
    """Downsizes an image to a maximum width/height, while keeping its aspect ratio"""
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def get_image_dimensions(
    path: str, as_string: bool = True
) -> Union[str, Tuple[int, int]]:
    """Returns the dimensions of an image, either as a string or a tuple"""
    img = Image.open(path)
    if as_string:
        return f"{img.width}x{img.height}px"
    else:
        return img.width, img.height


def image_as_html(image_field: str, max_width: int = 300, max_height: int = 300) -> str:
    """Returns the necessary HTML to display our image, with a maximum width/height."""
    html = ""
    relative_path = image_field.name
    if relative_path:
        # Getting the dimensions
        full_path = image_field.path
        width, height = get_image_dimensions(full_path, string=False)
        # Resizing based on width
        if width > max_width:
            coef = round(width / max_width, 2)
            width = max_width
            height = round(height / coef, 0)
        # Resizing based on height
        if height > max_height:
            coef = round(height / max_height, 2)
            height = max_height
            width = round(width / coef, 0)
        # Creating the HTML
        image_info = {
            "path": relative_path,
            "width": width,
            "height": height,
        }
        html = """
        <a href='/media/{path}' target='_blank'>
            <img src='/media/{path}' width='{width}px' height='{height}px'/>
        </a>
        """.format(
            **image_info
        )
    return mark_safe(html)
