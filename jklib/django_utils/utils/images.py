"""Functions for managing image files, mostly through the pillow/PIL
library."""
# Built-in
import base64
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

# Django
from django.core.files import File
from django.db.models import ImageField

# Third-party
from PIL import Image

IMAGE_TYPES = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def override_image_in_storage(img_field: ImageField, new_img: Image.Image) -> None:
    """Override image in storage."""
    img_filename = Path(img_field.file.name).name
    img_ext = img_filename.split(".")[-1]
    img_format = IMAGE_TYPES[img_ext]
    buffer = BytesIO()
    new_img.save(buffer, format=img_format)
    file_object = File(buffer)
    # Save the new resized file as usual, which will save to S3 using django-storages
    img_field.save(img_filename, file_object)


def downsize_image(file_path: str, width: int, height: int) -> None:
    """Downsizes an image to a maximum width/height, while keeping its aspect
    ratio."""
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def maybe_resize_image(
    img: Image.Image, max_size: Optional[int] = None
) -> Tuple[bool, Image.Image]:
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


def image_to_base64(data: ImageField) -> bytes:
    buffered = BytesIO()
    original_image = Image.open(data)
    original_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())


def resized_image_to_base64(data: ImageField, max_size: Optional[int] = None) -> bytes:
    buffered = BytesIO()
    original_image = Image.open(data)
    _, resized_image = maybe_resize_image(original_image, max_size=max_size)
    resized_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())
