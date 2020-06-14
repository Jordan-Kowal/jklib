"""DynamicSerializersMixin"""


class DynamicSerializersMixin:
    """
    Mixin to make the serializers dynamic, based on the action
    'serializer_classes' becomes useless and we will instead use [action].serializer
    """

    def get_serializer_class(self, *args, **kwargs):
        """Overridden to dynamically get the serializer from [action].serializer"""
        action_object = getattr(self, self.action)
        serializer_class = action_object.serializer
        return serializer_class
