"""Validators for model fields"""


# Django
from django.core.exceptions import ValidationError


# --------------------------------------------------------------------------------
# > Validator
# --------------------------------------------------------------------------------
def length_validator(min_=None, max_=None, trim=True):
    """
    Checks that the field length is within the provided limits
    :param int min_: The min length
    :param int max_: The max length
    :param bool trim: Whether to trim the value before the check. Defaults to True.
    :return: The check function
    :rtype: function
    """

    def check(value):
        """
        Performs the actual check with the provided arguments
        :raises ValidationError: If the text is not within the allowed ranges
        """
        if trim:
            value = value.strip()
        length = len(value)
        # Check min length
        if min_ is not None:
            if length < min_:
                raise ValidationError(
                    f"The text must be at least {min_}-character long"
                )
        # Check max length
        if max_ is not None:
            if length > max_:
                raise ValidationError(f"The text must be at most {max_}-character long")

    return check
