"""
Serializer and mixins classes for DRF
Split into sub-categories:
    Utility:                    Utility functions for serializers
    Mixins:                     Provide utility functions for serializers (but do not inherit from them)
    Base Serializers:           Improved DRF serializers through custom mixins and utility functions
    Ready-to-use Serializers:   Specific and re-usable serializers for common actions
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
    return {"required": True, "allow_null": False, "allow_blank": False}


def required_list():
    """
    Same as required, but for a LIST of items
    :return: Dict to set required, allow_blank, and allow_null to the right values
    :rtype: dict
    """
    return {"required": True, "allow_null": False, "allow_empty": False}


def optional():
    """
    To be used in a serializer's field customization. Makes the field optional
    :return: Dict to set required, allow_blank, and allow_null to the right values
    :rtype: dict
    """
    return {"required": False, "allow_null": True, "allow_blank": True}


def optional_list():
    """
    Same as optional, but for a LIST of items
    :return: Dict to set required, allow_blank, and allow_null to the right values
    :rtype: dict
    """
    return {"required": False, "allow_null": True, "allow_empty": True}


# --------------------------------------------------------------------------------
# > Mixins
# --------------------------------------------------------------------------------
class NoCreateMixin:
    """Mixin to remove the create workflow"""

    @staticmethod
    def create(validated_data):
        """Serializer cannot be used without an instance"""
        return NotImplemented()


class NoUpdateMixin:
    """Mixin to remove the update workflow"""

    @staticmethod
    def update(instance, validated_data):
        """Serializer cannot be used with an instance"""
        return NotImplemented()


# --------------------------------------------------------------------------------
# > Serializers
# --------------------------------------------------------------------------------
class ImprovedSerializer(serializers.Serializer):
    """Improved version of the DRF Serializer class with utility functions"""

    @property
    def required_fields(self):
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

    @staticmethod
    def check_is_not_empty(fieldname, value, message=None):
        """
        Checks if a field is empty (after trimming it)
        :param str fieldname: Name of the field
        :param str value: Current value of the field
        :param str message: The error message to display if the field is empty
        :raise ValidationError: If the field is empty
        :return: The not-empty trimmed string
        :rtype: str
        """
        if message is None:
            f"The '{fieldname}' field cannot be empty"
        value = value.strip()
        if value == "":
            raise serializers.ValidationError(message)
        return value

    def check_required_fields(self, validated_data):
        """
        Check that all required fields are present in the data
        :param dict validated_data: Validated data passed to the .validate() method
        :raise ValidationError: If some required fields are not in the validated_data
        """
        missing_fields = [
            field for field in self.required_fields if field not in validated_data
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
        :raise ValidationError: If we find an already existing model instance
        """
        # Defaulting some parameters
        if message is None:
            "A similar item already exists (and is linked to your user)"
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


class IdListSerializer(ImprovedSerializer):
    """Simple serializer that expects a list of IDs"""

    ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), **required_list()
    )
