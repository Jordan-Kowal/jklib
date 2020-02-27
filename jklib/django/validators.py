# coding: utf-8
"""
Description:
    Utility functions for validating model data
Functions:
    validate_past_date: Checks the given date is not in the future
    validate_postal_code: Checks the format of the postal code
    validate_siren: Checks that the SIREN contains 9 digits
"""


# Built-in
import re
from datetime import date

# Django
from django.core.exceptions import ValidationError


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def validate_past_date(value):
    """Checks the given date is not in the future"""
    if value > date.today():
        raise ValidationError("La date ne peut pas être dans le futur")


def validate_postal_code(value):
    """Checks the format of the postal code"""
    pattern = r"^\d?\d{4}"
    match = re.search(pattern, value)
    if match is None:
        raise ValidationError("Le code postal doit être composé de 4 ou 5 chiffres")


def validate_siren(value):
    """Checks that the SIREN contains 9 digits"""
    if len(value) != 9 or not value.isdigit():
        raise ValidationError("Merci de fournir un code SIREN valide (9 chiffres)")
