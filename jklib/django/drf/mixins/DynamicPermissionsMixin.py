"""DynamicPermissionsMixin"""


# Local
from ..permissions import BlockAll


class DynamicPermissionsMixin:
    """
    Mixin to make the permissions dynamic, based on the action
    'permission_class' becomes useless and we will instead use [action].permissions
    """

    def get_permissions(self):
        """
        Overrides the method to fetch permissions in [action].permissions
        If permissions are forgotten, defaults to "BlockAll" to avoid security breaches
        """
        if self.action is None:
            permissions = [BlockAll]
        else:
            action_object = getattr(self, self.action)
            permissions = getattr(action_object, "permissions", [BlockAll])
        return [permission() for permission in permissions]
