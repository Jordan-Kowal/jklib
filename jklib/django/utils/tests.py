"""Shared classes and functions for tests in Django and DRF"""

# Built-in
from string import ascii_letters, digits
from time import sleep

# Django
from django.core import mail
from django.test import RequestFactory, TestCase

# --------------------------------------------------------------------------------
# > Constants
# --------------------------------------------------------------------------------
CHARS = ascii_letters + digits


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def assert_logs(logger, level):
    """
    Wraps a test into a `self.assertLogs`. The `context` is available in self.logger_context.
    :param str logger: The logger to intercept
    :param str level: The minimum log level to look for
    :return: Decorator
    :rtype: func
    """
    level = level.upper()

    def decorator(function):
        def wrapper(self, *args, **kwargs):
            with self.assertLogs(logger=logger, level=level) as context:
                self.logger_context = context
                return function(self, *args, **kwargs)

        return wrapper

    return decorator


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ImprovedTestCase(TestCase):
    """Improvement from TestCase with various utilities"""

    # ----------------------------------------
    # Assertions
    # ----------------------------------------
    @staticmethod
    def assert_email_was_sent(
        subject, index=0, size=1, to=None, cc=None, cci=None, async_=True
    ):
        """
        Checks that ONE specific email has been sent (and is the only one sent)
        :param str subject: Subject of the email, used to find it in the mailbox
        :param bool async_: Whether it was sent asynchronously
        """
        if async_:
            sleep(0.2)
        email = mail.outbox[index]
        assert len(mail.outbox) == size
        assert email.subject == subject
        if to is not None:
            assert len(to) == len(email.to)
            assert set(to) == set(email.to)
        if cc is not None:
            assert len(cc) == len(email.cc)
            assert set(cc) == set(email.cc)
        if cci is not None:
            assert len(cci) == len(email.cci)
            assert set(cci) == set(email.cci)

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
