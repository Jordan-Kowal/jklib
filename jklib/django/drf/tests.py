"""Useful constants, functions, and classes for test management in DRF"""

# Django
from rest_framework.test import APIClient, APITestCase

# Local
from ..utils.network import build_url_with_params


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ActionTestCase(APITestCase):
    """
    TestCase class specifically for testing service built with our ActionHandler class
    Inherits from APITestCase and provides various utility functions
    """

    # ----------------------------------------
    # Properties
    # ----------------------------------------
    service_url = None
    required_fields = []

    # ----------------------------------------
    # Behavior
    # ----------------------------------------
    @classmethod
    def setup_class(cls):
        """Initializes the API client"""
        cls.client = APIClient()

    # ----------------------------------------
    # Assertions
    # ----------------------------------------
    def assert_fields_are_required(self, handler, url, valid_payload):
        """
        Tests that the provided fields are required for a request.
        For each field, we will:
            Use a valid payload
            Remove only the specific field
            Call the endpoint with that payload
            Expect a 400 HTTP status and an error for our field
        :param function handler:
        :param str url: The service url
        :param fields: The list of fields that are required
        :type fields: [str]
        :param dict valid_payload: A valid payload for the service
        """
        for field in self.required_fields:
            request_payload = valid_payload.copy()
            request_payload[field] = None
            response = handler(url, request_payload)
            self.assert_field_has_error(response, field)

    @staticmethod
    def assert_field_has_error(response, field, code=400, n=1):
        """
        Tests that a specific field has raised an error by checking:
            The error code
            That there's an error message for this field in the response
        :param Response response: Response from the server, following our query
        :param str field: The field we're looking for
        :param int code: The expected HTTP code
        :param int n: The minimum amount of errors expected for this field
        """
        assert response.status_code == code
        assert len(response.data[field]) >= n

    # ----------------------------------------
    # Utilities
    # ----------------------------------------
    def detail_url(self, object_id):
        """
        Builds a detail URL for an instance model
        :param int object_id: ID of our target instance
        :return: The detail URL for this service and instance
        :rtype: str
        """
        if self.service_url[-1] == "/":
            url = self.service[:-1]
        else:
            url = self.service
        return f"{url}/{object_id}"

    def detail_url_with_params(self, object_id, params):
        """
        Builds a detail URL for an instance model with added GET parameters
        :param int object_id: ID of our target instance
        :param dict params: The parameters to pass in the URL
        :return: The detail URL with GET params
        :rtype: str
        """
        detail_url = self.detail_url(object_id)
        return build_url_with_params(detail_url, params)

    def service_url_with_params(self, params):
        """
        Adds GET parameters to the service URL
        :param dict params: The parameters to pass in the URL
        :return: The service URL with GET params
        :rtype: str
        """
        return build_url_with_params(self.service_url, params)
