"""BaseAction"""


# Django
from rest_framework import exceptions


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class BaseAction:
    """
    Class for easier handling of viewset actions

    THINGS TO KNOW:
        You should call .run() to execute your action
        That will look up and run the method with the same name as the action method (post, get, etc.)
        If it doesn't exist, it will run .main()

    HOW TO USE:
        Create a new class that inherits from our Action class
        Override the "main" method or create specific method(s) based on action methods (post, get, etc.)
        Either way, that method should return a Response object (from DRF)
        In the viewset, create a new action like you normally would
        That action should simply returns YourActionClass.run()
    """

    def __init__(self, viewset, request, *args, **kwargs):
        """
        Initialize the instance  and sets up its attributes for later use
        Args:
            viewset (Viewset): Viewset object from DRF
            request (HttpRequest): Request object from Django
            *args (*): Any additional arg(s)
            **kwargs (*): Any additional kwarg(s)
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
        Returns:
            (HttpResponse): Response from DRF
        """
        action_to_run = getattr(self, self.method, self.main)
        return action_to_run()

    def run_action_from_super_view(self, action_name):
        """
        Calls an action from the parent viewset with the initial arguments
        Args:
            action_name (str): Name of the method to call
        Returns:
            (*) The results from the function call
        """
        parent_viewset_action = getattr(self.super_view(), action_name)
        return parent_viewset_action(self.request, *self.args, **self.kwargs)

    def super_view(self):
        """
        Equivalent to calling super() on the viewset
        Returns:
            (Viewset) The parent class of the viewset
        """
        return super(type(self.viewset), self.viewset)

    @staticmethod
    def main():
        """Default function for the service processing"""
        return exceptions.MethodNotAllowed()
