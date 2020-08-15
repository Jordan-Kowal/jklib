"""Useful constants, functions, and classes for test management in DRF"""

# Built-in
from random import choices, seed
from string import ascii_letters, digits

# Django
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

# Local
from ..utils.network import build_url_with_params

# --------------------------------------------------------------------------------
# > Constants
# --------------------------------------------------------------------------------
CHARS = ascii_letters + digits


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
    append_slash = True
    required_fields = []
    existing_random_values = set()

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
    # User fixtures
    # ----------------------------------------
    def create_user(self, authenticate=False, **kwargs):
        """
        Creates a user using the User object, and forces the username to match the email
        Random values will be added if some fields are missing
        :param bool authenticate: Whether to authenticate the user
        :param kwargs: Fields/Values for the User model
        :return: The created user
        :rtype: User
        """
        # Adds default values in "kwargs" for missing fields
        for field, value in self.generate_random_user_data().items():
            if kwargs.get(field) is None:
                kwargs[field] = value
        # Drops username as we'll replace it with the email
        kwargs.pop("username", None)
        email = kwargs.pop("email")
        user = User.objects.create_user(username=email, email=email, **kwargs)
        # Logs user is asked to
        if authenticate:
            self.client.force_authenticate(user)
        return user

    def create_admin_user(self, authenticate=False, **kwargs):
        """
        Creates a staff user. Simply call self.create_user() with "is_staff" set to true
        :return: The created admin user
        :rtype: User
        """
        kwargs["is_staff"] = True
        user = self.create_user(authenticate, **kwargs)
        return user

    def generate_random_user_data(self):
        """
        Returns a dict/payload that could be used to create a User instance
        The data is both randomly generated and unique
        :return: Valid dict for creating a User
        :rtype: dict
        """
        return {
            "email": self.generate_random_string(15, "@", 5, ".com"),
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(20),
            "first_name": self.generate_random_string(6),
            "last_name": self.generate_random_string(6),
        }

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
        url = self.service_url
        url = url[:-1] if url[-1] == "/" else url
        url = f"{url}/{object_id}"
        if self.append_slash:
            url += "/"
        return url

    def detail_url_with_params(self, object_id, params):
        """
        Builds a detail URL for an instance model with added GET parameters
        :param int object_id: ID of our target instance
        :param dict params: The parameters to pass in the URL
        :return: The detail URL with GET params
        :rtype: str
        """
        url = self.detail_url(object_id)
        url = build_url_with_params(url, params)
        if self.append_slash:
            url += "/"
        return url

    def service_url_with_params(self, params):
        """
        Adds GET parameters to the service URL
        :param dict params: The parameters to pass in the URL
        :return: The service URL with GET params
        :rtype: str
        """
        url = build_url_with_params(self.service_url, params)
        if self.append_slash:
            url += "/"
        return

    # ----------------------------------------
    # Others
    # ----------------------------------------
    def generate_random_string(self, *instructions):
        """
        Generates a random string based on the given instructions. There are 2 types of instructions:
            int: Will choose N characters from lowercase letters, uppercase letters, and digits
            str: Will simply use the given string
        The instructions are processed in the given order
        Once a string is built, we make sure it is unique by checking our vault
        If not unique, it is deleted and we try again
        :param instructions: Integers or strings to be used to generate our string
        :type instructions: int or str
        :return: The randomly generated and unique string
        :rtype: str
        """
        seed()
        while True:
            random_string = ""
            for element in instructions:
                if type(element) == int:
                    random_string += "".join(choices(CHARS, k=element))
                elif type(element) == str:
                    random_string += element
                else:
                    raise TypeError(
                        "generate_random_string() only accept 'int' or 'str' as individual instructions"
                    )
            if random_string not in self.existing_random_values:
                self.existing_random_values.add(random_string)
                break
        return random_string
