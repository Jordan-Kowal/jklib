from io import BytesIO
from pathlib import Path

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
    """Overrides an image in storage with a new image."""
    img_filename = Path(img_field.file.name).name
    img_ext = img_filename.split(".")[-1]
    img_format = IMAGE_TYPES[img_ext]
    buffer = BytesIO()
    new_img.save(buffer, format=img_format)
    file_object = File(buffer)
    img_field.save(img_filename, file_object)
