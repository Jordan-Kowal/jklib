"""Functions for managing image files, mostly through the pillow/PIL library"""

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
    :param str file_path: Path to the image file
    :param int width: Maximum width
    :param int height: Maximum height
    """
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def get_image_dimensions(path, string=True):
    """
    Returns the dimensions of an image, either as a string or a tuple
    :param str path: Path to the image file
    :param bool string: Indicates whether to return a str or a tuple. Defaults to True.
    :return: Either a string like "(width)x(height)px" or a tuple (width, height)
    :rtype: tuple(int, int) or str
    """
    img = Image.open(path)
    if string:
        return "{}x{}px".format(img.width, img.height)
    else:
        return (img.width, img.height)


def image_as_html(image_field, max_width=300, max_height=300):
    """
    Returns the necessary HTML to display our image, with a maximum width/height.
    :param str image_field: The name of the image field in our model instance
    :param int max_width: Maximum display width. Defaults to 300.
    :param int max_height: Maximum display height. Defaults to 300.
    :return: HTML string marked as safe for django
    :rtype: str
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
