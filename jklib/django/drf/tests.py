"""Useful constants, functions, and classes for test management in DRF"""

# Built-in
from urllib.parse import urlencode

# Django
from rest_framework.test import APIClient

# Local
from ..utils.tests import ImprovedTestCase


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ActionTestCase(ImprovedTestCase):
    """TestCase that provides utility for testing DRF actions/endpoints"""

    api_client_class = APIClient
    url_template = ""  # Use {{name}} for templating
    http_method_name = ""
    success_code = ""
    payload = None

    # ----------------------------------------
    # Behavior
    # ----------------------------------------
    @classmethod
    def setUpClass(cls):
        """Sets up the API client"""
        cls.api_client = cls.api_client_class()
        cls.http_method = getattr(cls.api_client, cls.http_method_name.lower())
        super(ActionTestCase, cls).setUpClass()

    # ----------------------------------------
    # Utilities
    # ----------------------------------------
    def url(self, context=None, params=None):
        """
        Builds a URL through a templating system
        :param dict context: Data to replace in the URL
        :param dict params: GET parameters to add in the URL
        :return: The generated endpoint URL
        :rtype: str
        """
        url = self.url_template
        if context is not None:
            for key, value in context.items():
                url = url.replace(f"{{{key}}}", str(value))
        if params is not None:
            if url[-1] == "/":
                url = url[:-1]
            url += urlencode(params)
        if url[-1] != "/":
            url += "/"
        if url[0] != "/":
            url = "/" + url
        return url.replace("//", "/")
