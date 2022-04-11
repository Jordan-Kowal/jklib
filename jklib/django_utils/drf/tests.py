"""Useful constants, functions, and classes for test management in DRF"""

# Built-in
from typing import Dict, Optional
from urllib.parse import urlencode

# Django
from rest_framework.test import APIClient

# Local
from ..utils.tests import ImprovedTestCase


class ActionTestCase(ImprovedTestCase):
    """TestCase that provides utility for testing DRF actions/endpoints"""

    api_client_class = APIClient
    url_template = ""  # Use {{name}} for templating
    http_method_name = ""
    success_code = ""
    payload = None

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the API client"""
        cls.api_client = cls.api_client_class()
        cls.http_method = getattr(cls.api_client, cls.http_method_name.lower())
        super().setUpClass()

    def build_url(
        self, context: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> str:
        """Builds a URL through a templating system"""
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
