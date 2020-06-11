"""Contains the Service class, for handling various services/action in a viewset"""

# Django
from rest_framework import exceptions


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Service:
    """
    Service class for handling the execution of a DRF service call. Provides various utility functions.
    To execute/run the service, call the "process" function. It will run either:
        - The function whose name matches the method (post, get, ...)
        - The default "service" function
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
        Runs either the function with the same name as the action (post, get, ...) or the default "service" function
        Returns:
            (HttpResponse): Response from Django
        """
        try:
            method = self.request.method.lower()
            process_service = getattr(self, method, self.service)
        except AttributeError:
            raise exceptions.MethodNotAllowed()
        return process_service()
