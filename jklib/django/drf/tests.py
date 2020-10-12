"""Useful constants, functions, and classes for test management in DRF"""

# Built-in
from time import sleep

# Django
from django.core import mail
from rest_framework.test import APIClient

# Local
from ..utils.network import build_url
from ..utils.tests import ImprovedTestCase


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ActionTestCase(ImprovedTestCase):
    """
    TestCase class specifically for testing service built with our ActionHandler class
    Inherits from ImprovedTestCase
    Provides the following:
        Assertions for required fields, field errors, and emails
        URL builder for services and detailed url
        User generation with authentication
    """

    # ----------------------------------------
    # Properties
    # ----------------------------------------
    client_class = APIClient
    service_base_url = ""  # Before the model id
    service_extra_url = ""  # After the model id

    # ----------------------------------------
    # Assertions
    # ----------------------------------------
    @staticmethod
    def assert_email_was_sent(subject, async_=True):
        """
        Checks that ONE specific email has been sent (and is the only one sent)
        :param str subject: Subject of the email, used to find it in the mailbox
        :param bool async_: Whether it was sent asynchronously
        """
        if async_:
            sleep(0.2)
        email = mail.outbox[0]
        assert len(mail.outbox) == 1
        assert email.subject == subject

    def assert_fields_are_required(self, handler, url, valid_payload, fields=None):
        """
        Tests that the provided fields are required for a request.
        For each field, we will:
            Use a valid payload
            Remove only the specific field
            Call the endpoint with that payload
            Expect a 400 HTTP status and an error for our field
        :param function handler:
        :param str url: The service url
        :param dict valid_payload: A valid payload for the service
        :param [str] fields: List of fields to check. Defaults to self.required_fields
        """
        if fields is None:
            fields = self.required_fields
        for field in fields:
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
    # URL utilities
    # ----------------------------------------
    def detail_url(self, object_id):
        """
        Builds a detail URL for an instance model
        :param int object_id: ID of our target instance
        :return: The detail URL for this service and instance
        :rtype: str
        """
        id_ = str(object_id)
        parts = [self.service_base_url, id_, self.service_extra_url]
        url = build_url(parts, end_slash=True)
        return f"/{url}"

    def detail_url_with_params(self, object_id, params):
        """
        Builds a detail URL for an instance model with added GET parameters
        :param int object_id: ID of our target instance
        :param dict params: The parameters to pass in the URL
        :return: The detail URL with GET params
        :rtype: str
        """
        id_ = str(object_id)
        parts = [self.service_base_url, id_, self.service_extra_url]
        url = build_url(parts, params=params, end_slash=True)
        return f"/{url}"

    def service_url_with_params(self, params):
        """
        Adds GET parameters to the service URL
        :param dict params: The parameters to pass in the URL
        :return: The service URL with GET params
        :rtype: str
        """
        parts = [self.service_base_url]
        url = build_url(parts, params=params, end_slash=True)
        return f"/{url}"

    # ----------------------------------------
    # User fixtures
    # ----------------------------------------
    def create_user(self, authenticate=False, **kwargs):
        """
        Creates a user and potentially authenticates the client with him
        The username will be set to the email address
        Any missing field will be randomly generated
        :param bool authenticate: Whether to authenticate the user
        :param kwargs: Fields/Values for the User model
        :return: The created user
        :rtype: User
        """
        user = super().create_user(**kwargs)
        if authenticate:
            self.client.force_authenticate(user)
        return user

    def create_admin_user(self, authenticate=False, **kwargs):
        """
        Same as self.create_user() except that 'is_staff' is forced to True
        :param bool authenticate: Whether to authenticate the user
        :param kwargs: Fields/Values for the User model
        :return: The created admin user
        :rtype: User
        """
        user = super().create_admin_user(**kwargs)
        if authenticate:
            self.client.force_authenticate(user)
        return user
