# coding: utf-8
"""
Description:
    Custom validator functions used throughout our API
Functions:
    check_missing_fields: Checks if all the required fields are in the request data
    check_unique_for_user: Checks if an element already exists for our user with the given parameters
    is_empty: Removes the spaces before/after and checks if the field is empty
"""


# Django
from django.db.models import Q
from rest_framework import serializers

# Local
from .serializers import get_required_fields


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def check_missing_fields(serializer, validated_data):
    """
    Validator to use in the .validate() method of a "normal" serializer
    Checks if all the required fields are in the request data
    """
    required_fields = get_required_fields(serializer)
    missing_fields = [field for field in required_fields if field not in validated_data]
    if missing_fields:
        message = "Les champs manquants sont : "
        message += "".join(missing_fields)
        raise serializers.ValidationError(message)


def check_unique_for_user(serializer, message, **params):
    """
    Description:
        Checks if an element already exists for our user with the given parameters
    Args:
        serializer (Serializer): Serializer instance from DRF
        message (str): The error message to display if an error is raised
        params (**kwargs): The query parameters to be used (with AND)
    Raises:
        serializers.ValidationError: Triggered if another instance is found
    """
    # Building the query
    user = serializer.context["request"].user
    query = Q(user=user) & Q(**params)
    if serializer.instance:
        query = query & ~Q(id=serializer.instance.id)
    # Checking the results
    model = serializer.Meta.model
    if model.objects.filter(query).exists():
        raise serializers.ValidationError(message)


def is_empty(field, message):
    """
    Description:
        Removes the spaces before/after and checks if the field is empty
        Returns the stripped field or raises an error
    Args:
        field (str): A string variable
        message (str): The error message to display if the field is empty
    Raises:
        serializers.ValidationError: Triggered when the field is empty
    Returns:
        str: The field stripped of its before/after spaces
    """
    field = field.strip()
    if not field:
        raise serializers.ValidationError(message)
    return field
