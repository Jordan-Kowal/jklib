"""Classes to make building actions/endpoints in DRF easier"""


# Django
from rest_framework.exceptions import MethodNotAllowed

# Local
from .permissions import BlockAll


# --------------------------------------------------------------------------------
# > Actions
# --------------------------------------------------------------------------------
class ActionHandler:
    """
    ---------- DESCRIPTION ----------
    Custom class for processing action calls, and also provides more flexibility for action customization
    This class must be used within the DynamicViewSet class we've created

    Permissions and Serializers must be defined at the class level, respectively in 'permissions' and 'serializers'
    Both can either directly contain the value, or be a dictionary with 1 value per method (get, post, ...)

    To process the action, call the .run() method. It will either:
        Call the [.get(), .post(), ...] function based on the action method
        Fallback on the .main() function if none of the above is found

    When initialized, the instance will store all the data from the request call, making it accessible at all times
    Also provides utility with .super_view() and .run_action_from_super_view()

    ---------- HOW TO SETUP ----------
    Make sure to define the following elements:
        permissions (direct or dict)
        serializers (direct or dict)
        [.get(), .post(), ...] if your action has several valid protocol/methods
        .main() if your action has a single method

    ---------- HOW TO USE: with DynamicViewSet ----------
    Simply match your actions with your ActionHandler classes, as described in the DynamicViewSet documentation
    The viewset will then take care of the rest
    """

    permissions = (BlockAll,)
    serializers = None

    def __init__(self, viewset, request, *args, **kwargs):
        """
        Initialize the instance  and sets up its attributes for later use
        :param ViewSet viewset: Viewset from DRF where our action will take place
        :param HttpRequest request: The request object from django that called our action
        :param args: Additional args automatically passed to our action
        :param kwargs: Additional kwargs automatically passed to our action
        """
        # Storing args
        self.viewset = viewset
        self.request = request
        self.args = args
        self.kwargs = kwargs
        # Useful shortcuts
        self.user = request.user
        self.data = request.data
        self.method = request.method.lower()

    def run(self):
        """
        Process the service request by calling the appropriate method
        It will look for a function matching the [method] name and will default to the "main" function
        :return: Response instance from DRF, containing our results
        :rtype: Response
        """
        action_to_run = getattr(self, self.method, self.main)
        return action_to_run()

    def run_action_from_super_view(self, action_name):
        """
        Calls an action from the parent viewset with the initial arguments
        :param str action_name: Name of the method to call from the parent viewset
        :return: The results from the parent function we called
        """
        parent_viewset_action = getattr(self.super_view(), action_name)
        return parent_viewset_action(self.request, *self.args, **self.kwargs)

    def super_view(self):
        """
        Equivalent to calling super() on the viewset
        :return: The parent class of the viewset
        :rtype: ViewSet
        """
        return super(type(self.viewset), self.viewset)

    @staticmethod
    def main():
        """Default function for the service processing"""
        return MethodNotAllowed()
