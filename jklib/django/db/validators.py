"""Validators for model fields"""


# Django
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# --------------------------------------------------------------------------------
# > Validators
# --------------------------------------------------------------------------------
@deconstructible
class LengthValidator:
    """Validator that can check the min and/or max length of a field"""

    message = ""  # Depends on args

    def __init__(self, min_=None, max_=None, trim=True):
        """
        Sets the instance attributes
        :param int min_: The min length
        :param int max_: The max length
        :param bool trim: Whether to trim the value before the check. Defaults to True.
        """
        self.min_ = min_
        self.max_ = max_
        self.trim = trim

    def __call__(self, value):
        """
        Checks if the value meets the length criterion
        :param str value: The current string value of the field
        :raise ValidationError: If the field is either too short or too long
        """
        if self.trim:
            value = value.strip()
        length = len(value)
        # Check min length
        if self.min_ is not None:
            if length < self.min_:
                self.message = f"The text must be at least {self.min_}-character long"
                raise ValidationError(self.message)
        # Check max length
        if self.max_ is not None:
            if length > self.max_:
                self.message = f"The text must be at most {self.max_}-character long"
                raise ValidationError(self.message)
