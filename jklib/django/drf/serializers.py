"""
Serializer and mixins classes for DRF
Split into sub-categories:
    Utility: Utility functions for serializers
    Mixins: Provide utility functions for serializers (but do not inherit from them)
    Serializers: Improved DRF serializers through custom mixins and utility functions
"""


# Django
from django.db.models import Q
from rest_framework import serializers


# --------------------------------------------------------------------------------
# > Utility
# --------------------------------------------------------------------------------
def required():
    """
    To be used in a serializer's field customization. Makes the field mandatory
    :return: Dict to set required, allow_blank, and allow_null to the right values
    :rtype: dict
    """
    return {"required": True, "allow_blank": False, "allow_null": False}


# --------------------------------------------------------------------------------
# > Mixins
# --------------------------------------------------------------------------------
class NotEmptyMixin:
    """Provides .validate() that raises an error if data is empty"""

    @staticmethod
    def validate(validated_data):
        """Raises an error if validated_data is empty"""
        if not validated_data:
            message = "Aucune donnée n'a été fournie"
            raise serializers.ValidationError(message)
        return validated_data


# --------------------------------------------------------------------------------
# > Serializers
# --------------------------------------------------------------------------------
class ImprovedSerializer(serializers.Serializer):
    """Improved version of the DRF Serializer class with utility functions"""

    def check_required_fields(self, validated_data):
        """
        Check that all required fields are present in the data
        :param dict validated_data: Validated data passed to the .validate() method
        :raises ValidationError: If some required fields are not in the validated_data
        """
        required_fields = self._get_serializer_required_fieldnames()
        missing_fields = [
            field for field in required_fields if field not in validated_data
        ]
        if missing_fields:
            message = f"The following fields are required: {', '.join(missing_fields)}"
            raise serializers.ValidationError(message)

    def check_unique_for_user(self, message=None, model=None, **params):
        """
        Checks if an object with specific params do not already exists for our user
        :param str message: The error message if a similar model instance already exist
        :param Model model: The model class we will check for the unique constraint. Defaults to Meta.model
        :param params: The query parameters to fetch the maybe-existing model instance
        :raises ValidationError: If we find an already existing model instance
        """
        # Defaulting some parameters
        if message is None:
            f"A similar item already exists and is attach to your profile"
        if model is None:
            model = self.Meta.model
        # Building the query
        user = self.context["request"].user
        query = Q(user=user) & Q(**params)
        if self.instance:
            query = query & ~Q(id=self.instance.id)
        # Checking the results
        if model.objects.filter(query).exists():
            raise serializers.ValidationError(message)

    @staticmethod
    def check_is_not_empty(fieldname, value, message=None):
        """
        Checks if a field is empty (after trimming it)
        :param str fieldname: Name of the field
        :param str value: Current value of the field
        :param str message: The error message to display if the field is empty
        :return: The not-empty trimmed string
        :rtype: str
        """
        if message is None:
            f"The '{fieldname}' field cannot be empty"
        value = value.strip()
        if value == "":
            raise serializers.ValidationError(message)
        return value

    # ----------------------------------------
    # Private
    # ----------------------------------------
    def _get_serializer_required_fieldnames(self):
        """
        Fetches the required fieldnames from the serializer
        :return: List of fieldnames that are required
        :rtype: list
        """
        required_fields = []
        for key, kwargs in self.fields.items():
            if kwargs.required:
                required_fields.append(key)
        return required_fields
