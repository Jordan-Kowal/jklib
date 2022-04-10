"""Shared classes and functions for tests in Django and DRF"""

# Built-in
from string import ascii_letters, digits
from time import sleep
from typing import Any, Callable, Dict, List, Optional

# Django
from django.core import mail
from django.test import RequestFactory, TestCase
from rest_framework.request import Request

CHARS = ascii_letters + digits


def assert_logs(logger: str, level: str) -> Callable:
    """Wraps a test into a `self.assertLogs`. The `context` is available in self.logger_context"""
    level = level.upper()

    def decorator(function: Callable) -> Callable:
        def wrapper(self: TestCase, *args, **kwargs) -> Any:
            with self.assertLogs(logger=logger, level=level) as context:
                self.logger_context = context
                return function(self, *args, **kwargs)

        return wrapper

    return decorator


class ImprovedTestCase(TestCase):
    """Improvement from TestCase with various utilities"""

    def assert_email_was_sent(
        self,
        subject: str,
        index: int = 0,
        size: int = 1,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        async_: bool = True,
    ) -> None:
        """Checks that ONE specific email has been sent (and is the only one sent)"""
        if async_:
            sleep(0.1)
        email = mail.outbox[index]
        self.assertEquals(len(mail.outbox), size)
        self.assertEquals(email.subject, subject)
        if to is not None:
            self.assertEquals(len(to), len(email.to))
            self.assertSetEqual(set(to), set(email.to))
        if cc is not None:
            self.assertEquals(len(cc), len(email.cc))
            self.assertSetEqual(set(cc), set(email.cc))
        if bcc is not None:
            self.assertEquals(len(bcc), len(email.bcc))
            self.assertSetEqual(set(bcc), set(email.bcc))

    @staticmethod
    def build_fake_request(
        method: str = "get", path: str = "/", data: Dict = None
    ) -> Request:
        """Creates and returns a fake request object"""
        factory = RequestFactory()
        factory_call = getattr(factory, method.lower())
        return factory_call(path, data=data)
