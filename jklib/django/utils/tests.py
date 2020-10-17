"""Shared classes and functions for tests in Django and DRF"""

# Built-in
from random import choices, seed
from string import ascii_letters, digits
from time import sleep

# Django
from django.contrib.auth.models import User
from django.core import mail
from django.test import RequestFactory, TestCase

# --------------------------------------------------------------------------------
# > Constants
# --------------------------------------------------------------------------------
CHARS = ascii_letters + digits


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ImprovedTestCase(TestCase):
    """
    Improvement from TestCase with various utilities:
        Assertion functions
        Several ways to create users
        Random data generation (data is stored to avoid generating the same value twice)
    """

    # ----------------------------------------
    # Properties
    # ----------------------------------------
    required_fields = []
    existing_random_values = set()

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

    # ----------------------------------------
    # User fixtures
    # ----------------------------------------
    def create_user(self, **kwargs):
        """
        Creates a user using the User object, and forces the username to match the email
        Random values will be added if some fields are missing
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
        return user

    def create_admin_user(self, **kwargs):
        """
        Creates a staff user. Simply call self.create_user() with "is_staff" set to true
        :param kwargs: Fields/Values for the User model
        :return: The created admin user
        :rtype: User
        """
        kwargs["is_staff"] = True
        user = self.create_user(**kwargs)
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
    # Others
    # ----------------------------------------
    @staticmethod
    def build_fake_request(method="get", path="/", data=None):
        """
        Creates and returns a fake request object
        :param str method: The name of the HTTP method to call in our factory
        :param str path: Target URL for the request
        :param dict data: Data to pass in the request
        :return: Returns a fake Request object
        :rtype: Request
        """
        factory = RequestFactory()
        factory_call = getattr(factory, method.lower())
        return factory_call(path, data=data)

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
