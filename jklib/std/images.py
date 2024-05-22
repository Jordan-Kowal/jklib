import base64
from io import BytesIO
from typing import Optional, Tuple

from PIL import Image


def downsize_image(file_path: str, width: int, height: int) -> None:
    """Downsizes an image to the given dimensions while keeping its ratio."""
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def image_to_base64(data: str) -> bytes:
    """Converts an image to base64."""
    buffered = BytesIO()
    original_image = Image.open(data)
    original_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())


def maybe_resize_image(
    img: Image.Image, max_size: Optional[int] = None
) -> Tuple[bool, Image.Image]:
    """Resizes an image to the given max size while keeping its ratio."""
    min_length, max_length = sorted([img.width, img.height])
    resized = False
    if max_length > max_size:
        factor = round(max_size * min_length / max_length)
        dimensions = (
            (max_size, factor) if img.width == max_length else (factor, max_size)
        )
        img = img.resize(dimensions)
        resized = True
    return resized, img


def resized_image_to_base64(data: str, max_size: Optional[int] = None) -> bytes:
    """Resizes an image to the given max size and converts it to base64."""
    buffered = BytesIO()
    original_image = Image.open(data)
    _, resized_image = maybe_resize_image(original_image, max_size=max_size)
    resized_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())
