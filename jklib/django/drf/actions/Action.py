"""Action"""


# Django
from rest_framework import exceptions


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Action:
    """
    Service class for handling the execution of a DRF service call. Provides various utility functions.
    Here's the desired workflow for creating a service
        - Create a new class that inherits from this Service class
        - Adds either the "service" function or a protocol (post/get/put/...) function
        - (That function should take care of handling the Request and returning the Response)
        - In the viewset, create a new action
        - That action should simply call "OurService.process()"
    """

    def __init__(self, viewset, request, *args, **kwargs):
        """
        Sets up the attributes for later use
        These are the 4 parameters receive when a DRF service is called
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
        self.method = request.method

    def run(self):
        """
        Process the service request by calling the appropriate method
        It will look for a function matching the [method] name and will default to the "main" function
        This should before the actual processing of the initial request and return a Response object
        Returns:
            (HttpResponse): Response from Django
        """
        method = self.request.method.lower()
        action_to_run = getattr(self, method, self.main)
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
