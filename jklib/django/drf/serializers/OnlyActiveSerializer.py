"""OnlyActiveSerializer"""


# Django
from rest_framework import serializers


class OnlyActiveSerializer(serializers.ListSerializer):
    """Filters the serializer based on the 'active' field"""

    def to_representation(self, data):
        """How the data is represented"""
        data = data.filter(active=True)
        return super(OnlyActiveSerializer, self).to_representation(data)
