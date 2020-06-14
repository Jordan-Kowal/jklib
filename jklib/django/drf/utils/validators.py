"""
Function for validating data, mostly used in Serializers
Validators:
    check_missing_fields: Checks if all the required fields are in the request data
    check_unique_for_user: Checks if an element already exists for our user with the given parameters
    is_empty: Removes the spaces before/after and checks if the field is empty
Private:
    _get_serializer_required_fieldnames: Returns the list of fieldnames that are required
"""


# Django
from django.db.models import Q
from rest_framework import serializers


# --------------------------------------------------------------------------------
# > Validators
# --------------------------------------------------------------------------------
def check_missing_fields(serializer, validated_data):
    """
    Validator to use in the .validate() method of a "normal" serializer
    Checks if all the required fields are in the request data
    """
    required_fields = _get_serializer_required_fieldnames(serializer)
    missing_fields = [field for field in required_fields if field not in validated_data]
    if missing_fields:
        message = f"Missing fields: {', '.join(missing_fields)}"
        raise serializers.ValidationError(message)


def check_unique_for_user(serializer, message=None, **params):
    """
    Checks if an element already exists for our user with the given parameters
    Args:
        serializer (Serializer): Serializer instance from DRF
        message (str, optional): The error message to display if an error is raised
        params (**kwargs): The query parameters to be used (with AND)
    Raises:
        serializers.ValidationError: Triggered if another instance is found
    """
    # Defaulting 'message'
    if message is None:
        f"A similar item already exists and is attach to your profile"
    # Building the query
    user = serializer.context["request"].user
    query = Q(user=user) & Q(**params)
    if serializer.instance:
        query = query & ~Q(id=serializer.instance.id)
    # Checking the results
    model = serializer.Meta.model
    if model.objects.filter(query).exists():
        raise serializers.ValidationError(message)


def check_is_not_empty(fieldname, value, message=None):
    """
    Removes the spaces before/after and checks if the field is empty
    Returns the stripped field or raises an error
    Args:
        fieldname (str): Name of the field
        value (str): Value of the field
        message (str, optional): The error message to display if the field is empty
    Raises:
        serializers.ValidationError: Triggered when the field is empty
    Returns:
        (str) The field stripped of its before/after spaces
    """
    if message is None:
        f"The '{fieldname}' field cannot be empty"
    value = value.strip()
    if value == "":
        raise serializers.ValidationError(message)
    return value


# --------------------------------------------------------------------------------
# > Private
# --------------------------------------------------------------------------------
def _get_serializer_required_fieldnames(serializer):
    """
    Returns the list of fieldnames that are required
    Args:
        serializer (Serializer): Serializer instance from DRF
    Returns:
        (list) List of fieldnames
    """
    required_fields = []
    for key, kwargs in serializer.fields.items():
        if kwargs.required:
            required_fields.append(key)
    return required_fields
