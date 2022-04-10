"""Serializers and mixins classes for DRF"""


# Built-in
from typing import Any, Dict, List, Optional, Type

# Django
from django.db.models import Model, Q
from rest_framework import serializers


def required() -> Dict[str, bool]:
    """To be used in a serializer's field customization. Makes the field mandatory"""
    return {"required": True, "allow_null": False, "allow_blank": False}


def required_list() -> Dict[str, bool]:
    """Same as required, but for a LIST of items"""
    return {"required": True, "allow_null": False, "allow_empty": False}


def optional() -> Dict[str, bool]:
    """To be used in a serializer's field customization. Makes the field optional"""
    return {"required": False, "allow_null": True, "allow_blank": True}


def optional_list() -> Dict[str, bool]:
    """Same as optional, but for a LIST of items"""
    return {"required": False, "allow_null": True, "allow_empty": True}


class NoCreateMixin:
    """Mixin to remove the create workflow"""

    @staticmethod
    def create(validated_data: Dict) -> Any:
        """Serializer cannot be used without an instance"""
        raise NotImplementedError


class NoUpdateMixin:
    """Mixin to remove the update workflow"""

    @staticmethod
    def update(instance, validated_data: Dict) -> Any:
        """Serializer cannot be used with an instance"""
        raise NotImplementedError


class ImprovedSerializer(serializers.Serializer):
    """Improved version of the DRF Serializer class with utility functions"""

    @property
    def required_fields(self) -> List[str]:
        """Fetches the required fieldnames from the serializer"""
        required_fields = []
        for key, kwargs in self.fields.items():
            if kwargs.required:
                required_fields.append(key)
        return required_fields

    @staticmethod
    def check_is_not_empty(
        fieldname: str, value: str, message: Optional[str] = None
    ) -> str:
        """Checks if a field is empty (after trimming it)"""
        if message is None:
            f"The '{fieldname}' field cannot be empty"
        value = value.strip()
        if value == "":
            raise serializers.ValidationError(message)
        return value

    def check_required_fields(self, validated_data: Dict) -> None:
        """Check that all required fields are present in the data"""
        missing_fields = [
            field for field in self.required_fields if field not in validated_data
        ]
        if missing_fields:
            message = f"The following fields are required: {', '.join(missing_fields)}"
            raise serializers.ValidationError(message)

    def check_unique_for_user(
        self,
        message: Optional[str] = None,
        model: Optional[Type[Model]] = None,
        **params,
    ) -> None:
        """Checks if an object with specific params do not already exists for our user"""
        # Defaulting some parameters
        if message is None:
            "A similar item already exists (and is linked to your user)"
        if model is None:
            model = self.Meta.model  # type: ignore
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
