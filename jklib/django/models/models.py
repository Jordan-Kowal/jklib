# coding: utf-8
"""
Contains useful function for managing models.
Models:
    ContentModel: Abstract model for 'Content tables' that adds 3 new fields.
    ModelWithImage: Abstract model that provides 3 dynamic properties for the "image" field
"""


# Django
from django.db import models

# Personal
from jklib.std.files import get_size

# Local
from ..images import get_image_dimensions, image_as_html
from .fields import ActiveField, DateCreatedField, DateUpdatedField


# --------------------------------------------------------------------------------
# > Models
# --------------------------------------------------------------------------------
class ContentModel(models.Model):
    """
    Abstract model for 'Content tables' that adds 3 new fields
    A 'Content model' is a model that stores content, as opposed to lookup tables
    The 3 new fields are: active, date_create, and date_updated
    """

    # ----------------------------------------
    # Fields
    # ----------------------------------------
    active = ActiveField()
    create_at = DateCreatedField()
    updated_at = DateUpdatedField()

    # ----------------------------------------
    # META, str, save, get_absolute_url
    # ----------------------------------------
    class Meta:
        """Metadata to configure our model in the database"""

        abstract = True


class ModelWithImage(models.Model):
    """
    Abstract model that provides 3 dynamic properties for the "image" field
    It should be used whenever a model has an ImageField
    """

    # ----------------------------------------
    # META, str, save, get_absolute_url
    # ----------------------------------------
    class Meta:
        """Metadata to configure our model in the database"""

        abstract = True

    # ----------------------------------------
    # Custom Properties
    # ----------------------------------------
    def image_dimensions(self):
        """
        Gets the dimensions of the image, either as a string or a tuple
        Returns:
            (str|tuple) Dimensions of the image
        """
        return get_image_dimensions(self.image.path)

    image_dimensions.short_description = "Dimensions"

    def image_size(self):
        """
        Returns the size of the image as KB
        Returns:
            (str) Image size with KB units
        """
        size = get_size(self.image.path)
        message = f"{size} KB"
        return message

    image_size.short_description = "Taille"

    def view_image(self):
        """
        Returns HTML code to display the image in a web browser
        Returns:
            (str) HTML snippet to display the image
        """
        return image_as_html(self.image)

    view_image.short_description = "Image actuelle"
