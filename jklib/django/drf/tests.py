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
    # Assertions
    # ----------------------------------------
    def assert_admin_permissions(self, url, payload=None):
        """
        Checks that the service is only available to admin users
        :param str url: The target url
        :param dict payload: The data to pass to the request
        """
        admin = self.create_admin_user()
        user = self.create_user()
        # 401 Not authenticated
        self.api_client.logout()
        response = self.http_method(url, data=payload)
        assert response.status_code == 401
        # 403 Not admin
        self.api_client.force_authenticate(user)
        response = self.http_method(url, data=payload)
        assert response.status_code == 403
        # 201 Admin
        self.api_client.logout()
        self.api_client.force_authenticate(admin)
        response = self.http_method(url, data=payload)
        assert response.status_code == self.success_code

    def assert_fields_are_required(self, url, valid_payload, fields=None):
        """
        Tests that the provided fields are required for a request
        :param str url: The service url
        :param dict valid_payload: A valid payload for the service
        :param [str] fields: List of fields to check. Defaults to self.required_fields
        """
        if fields is None:
            fields = self.required_fields
        for field in fields:
            request_payload = valid_payload.copy()
            request_payload[field] = None
            response = self.http_method(url, request_payload)
            assert response.status_code == 400
            assert len(response.data[field]) > 0

    # ----------------------------------------
    # URL utilities
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

    # ----------------------------------------
    # User fixtures
    # ----------------------------------------
    def create_user(self, authenticate=False, **kwargs):
        """
        Creates a user and maybe authenticates him
        :param bool authenticate: Whether to authenticate the user
        :param kwargs: Fields/Values for the User model
        :return: The created user
        :rtype: User
        """
        user = super().create_user(**kwargs)
        if authenticate:
            self.api_client.force_authenticate(user)
        return user

    def create_admin_user(self, authenticate=False, **kwargs):
        """
        Creates an admin ser and maybe authenticates him
        :param bool authenticate: Whether to authenticate the user
        :param kwargs: Fields/Values for the User model
        :return: The created admin user
        :rtype: User
        """
        user = super().create_admin_user(**kwargs)
        if authenticate:
            self.api_client.force_authenticate(user)
        return user
