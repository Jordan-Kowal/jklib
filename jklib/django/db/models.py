"""Classes and mixins for django models"""


# Local
from ...std.files import get_size
from ..utils.images import get_image_dimensions, image_as_html
from .fields import DateCreatedField, DateUpdatedField


# --------------------------------------------------------------------------------
# > Models
# --------------------------------------------------------------------------------
class LifeCycleMixin:
    """Model mixin that provides lifecycle fields for creation and update"""

    # ----------------------------------------
    # Fields
    # ----------------------------------------
    created_at = DateCreatedField()
    updated_at = DateUpdatedField()


class WithImageMixin:
    """Model mixin that provides custom property for a field named "image"""

    # ----------------------------------------
    # Custom Properties
    # ----------------------------------------
    def image_dimensions(self):
        """
        Gets the dimensions of the image, either as a string or a tuple
        :return: Dimensions of the image
        :rtype: str or tuple
        """
        return get_image_dimensions(self.image.path)

    image_dimensions.short_description = "Dimensions"

    def image_size(self):
        """
        Returns the size of the image as KB
        :return: Size of the image in KB
        :rtype: str
        """
        size = get_size(self.image.path)
        message = f"{size} KB"
        return message

    image_size.short_description = "Taille"

    def view_image(self):
        """
        Returns HTML code to display the image in a web browser
        :return: HTML code snippet to display the image
        :rtype: str
        """
        return image_as_html(self.image)

    view_image.short_description = "Image actuelle"
