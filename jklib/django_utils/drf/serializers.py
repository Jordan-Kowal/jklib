"""Serializers and mixins classes for DRF."""


# Built-in
from typing import Any, Dict

# Django
from django.db.models import Model
from rest_framework import serializers


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data: Dict[str, Any]) -> Model:
        raise NotImplementedError

    def update(self, instance: Model, validated_data: Dict[str, Any]) -> Model:
        raise NotImplementedError
