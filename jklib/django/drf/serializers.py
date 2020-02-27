# coding: utf-8
"""
Description:
    Custom serializer classes to be used in our API
Serializers:
    NotEmptySerializer: Provides .validate() that raises an error if data is empty
List Serializers:
    OnlyActiveSerializer: Filters the serializer based on the 'active' field
Utility functions
    get_required_fields: Returns the list of fieldnames that are required
"""


# Django
from rest_framework import serializers


# --------------------------------------------------------------------------------
# > Serializers
# --------------------------------------------------------------------------------
class NotEmptySerializer(serializers.BaseSerializer):
    """Provides .validate() that raises an error if data is empty"""

    def validate(self, validated_data):
        """Raises an error if validated_data is empty"""
        if not validated_data:
            message = "Aucune donnée n'a été fournie"
            raise serializers.ValidationError(message)
        return validated_data


# --------------------------------------------------------------------------------
# > List Serializers
# --------------------------------------------------------------------------------
class OnlyActiveSerializer(serializers.ListSerializer):
    """Filters the serializer based on the 'active' field"""

    def to_representation(self, data):
        """How the data is represented"""
        data = data.filter(active=True)
        return super(OnlyActiveSerializer, self).to_representation(data)


# --------------------------------------------------------------------------------
# > Utility functions
# --------------------------------------------------------------------------------
def get_required_fields(serializer):
    """Returns the list of fieldnames that are required"""
    required_fields = []
    for key, kwargs in serializer.fields.items():
        if kwargs.required:
            required_fields.append(key)
    return required_fields
