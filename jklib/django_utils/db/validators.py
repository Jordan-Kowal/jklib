"""Validators for Django model fields."""


# Built-in
from typing import Optional

# Django
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class LengthValidator:
    """Validator that can check the min and/or max length of a field."""

    message: str = ""  # Depends on args

    def __init__(
        self, min_: Optional[int] = None, max_: Optional[int] = None, trim: bool = True
    ) -> None:
        """Sets the instance attributes."""
        if min_ is None and max_ is None:
            raise ValueError("You need to provide at least a min or max length")
        self.min_: Optional[int] = min_
        self.max_: Optional[int] = max_
        self.trim: bool = trim

    def __call__(self, value: str) -> None:
        """Checks if the value meets the length criterion."""
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
