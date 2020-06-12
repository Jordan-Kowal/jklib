"""Contains the Service class, for handling various services/action in a viewset"""

# Django
from rest_framework import exceptions


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Service:
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

    def process(self):
        """
        Main function to use within the viewset action definition
        Runs either the function with the same name as the action (post, get, ...) or the default "service" function
        Returns:
            (HttpResponse): Response from Django
        """
        method = self.request.method.lower()
        process_service = getattr(self, method, self.service)
        return process_service()

    def service(self):
        """
        Either override this method, or provide specific action methods like "post", "get", etc.
        By default, return a "403 Method not allowed"
        Returns:
            (HttpResponse): Response from Django
        """
        raise exceptions.MethodNotAllowed()

    def service_from_super_view(self, action_name):
        """
        Calls an action from the parent viewset with the initial arguments
        Args:
            action_name (string): Name of the method to call
        Returns:
            (*) The results from the function call
        """
        parent_viewset_service = getattr(self.super_view(), action_name)
        return parent_viewset_service(self.request, *self.args, **self.kwargs)

    def super_view(self):
        """
        Equivalent to calling super() on the viewset
        Returns:
            (Viewset) The parent class of the viewset
        """
        return super(type(self.viewset), self.viewset)
