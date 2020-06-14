"""NotEmptySerializer"""


# Django
from rest_framework import serializers


class NotEmptySerializer(serializers.BaseSerializer):
    """Provides .validate() that raises an error if data is empty"""

    def validate(self, validated_data):
        """Raises an error if validated_data is empty"""
        if not validated_data:
            message = "Aucune donnée n'a été fournie"
            raise serializers.ValidationError(message)
        return validated_data
