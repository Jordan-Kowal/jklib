"""
Contains useful functions for managing image files, mostly through "pillow".
Functions:
    downsize_image: Downsizes an image to a maximum width/height, while keeping its aspect ratio
    get_image_dimensions: Returns the dimensions of an image, either as a string or a tuple
    image_as_html: Returns the necessary HTML to display our image, with a maximum width/height
    image_list_as_html: Returns a HTML snippet with several <img> tags to display our images
"""


# Django
from django.utils.safestring import mark_safe

# Third-party
from PIL import Image


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def downsize_image(file_path, width, height):
    """
    Downsizes an image to a maximum width/height, while keeping its aspect ratio
    Args:
        file_path (str): Path to the image file
        width (int): Maximum width
        height (int): Maximum height
    """
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def get_image_dimensions(path, string=True):
    """
    Returns the dimensions of an image, either as a string or a tuple
    Args:
        path (str): Path to the image file
        string (bool, optional): Indicates whether to return a str or a tuple. Defaults to True.
    Returns:
        (str/tuple) Either a string like "(width)x(height)px" or a tuple (width, height)
    """
    img = Image.open(path)
    if string:
        return "{}x{}px".format(img.width, img.height)
    else:
        return (img.width, img.height)


def image_as_html(image_field, max_width=300, max_height=300):
    """
    Returns the necessary HTML to display our image, with a maximum width/height.
    This function keeps the aspect-ratio when resizing.
    Resizing is done in CSS. The actual file remains unchanged.
    Args:
        image_field (str): ImageField instance from our model
        max_width (int, optional): Maximum display width. Defaults to 300.
        max_height (int, optional): Maximum display height. Defaults to 300.
    Returns:
        (str) HTML string marked as safe for django
    """
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
