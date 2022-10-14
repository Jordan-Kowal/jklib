"""Shared classes and functions for tests in Django and DRF."""
# Built-in
import datetime
import json
from string import ascii_letters, digits
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    OrderedDict,
    Type,
    Union,
)

# Django
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import FileField, Model, QuerySet
from django.test import RequestFactory, TestCase
from rest_framework.request import Request

CHARS = ascii_letters + digits


def assert_logs(logger: str, level: str) -> Callable:
    """Wraps a test into a `self.assertLogs`.

    The `context` is available in self.logger_context
    """
    level = level.upper()

    def decorator(function: Callable) -> Callable:
        def wrapper(self: TestCase, *args, **kwargs) -> Any:
            with self.assertLogs(logger=logger, level=level) as context:
                self.logger_context = context
                return function(self, *args, **kwargs)

        return wrapper

    return decorator


class ImprovedTestCase(TestCase):
    """Improvement from TestCase with various utilities."""

    def assertEmailWasSent(
        self,
        subject: str,
        to: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> None:
        email = mail.outbox[-1]
        self.assertEqual(email.subject, subject)
        if to is not None:
            self.assertEqual(len(to), len(email.to))
            self.assertSetEqual(set(to), set(email.to))
        if cc is not None:
            self.assertEqual(len(cc), len(email.cc))
            self.assertSetEqual(set(cc), set(email.cc))
        if bcc is not None:
            self.assertEqual(len(bcc), len(email.bcc))
            self.assertSetEqual(set(bcc), set(email.bcc))

    def assertFileEqual(
        self,
        file_1: Union[FileField, SimpleUploadedFile],
        file_2: Union[FileField, SimpleUploadedFile],
    ) -> None:
        # Reset cursor position to make sure we compare the whole file
        file_1.seek(0)
        file_2.seek(0)
        # .read() must be stored within variable or it won't work
        content_1 = file_1.read()
        content_2 = file_2.read()
        self.assertEqual(content_1, content_2)

    def assertQuerySetPks(
        self, queryset: QuerySet, expected_pks=Iterable[Any], pk="id"
    ) -> None:
        queryset_pks = {getattr(item, pk) for item in queryset}
        self.assertSetEqual(queryset_pks, set(expected_pks))

    def assertDateEqualsString(
        self,
        instance_date: Optional[Union[datetime.datetime, datetime.date]],
        string_date: Optional[str],
        format: Optional[str] = "%Y-%m-%dT%H:%M:%S.%fZ",
    ):
        if not instance_date:
            self.assertIsNone(string_date)
        else:
            self.assertEqual(instance_date.strftime(format), string_date)

    @staticmethod
    def build_fake_request(
        method: str = "get", path: str = "/", data: Dict = None
    ) -> Request:
        """Creates and returns a fake request object."""
        factory = RequestFactory()
        factory_call = getattr(factory, method.lower())
        return factory_call(path, data=data)

    @staticmethod
    def generate_non_existing_id(model: Type[Model]) -> Any:
        instance = model.objects.all().order_by("-id").first()
        return 1 if not instance else instance.id + 1

    @staticmethod
    def uploaded_file_from_path(
        filepath: str, upload_name: Optional[str] = None
    ) -> SimpleUploadedFile:
        """Uploads and returns a file object for a Django FileField."""
        if upload_name is None:
            upload_name = filepath.split("/")[-1]
        with open(filepath, "rb") as f:
            binary_content = f.read()
        return SimpleUploadedFile(
            name=upload_name,
            content=binary_content,
        )

    @classmethod
    def ordered_dict_to_dict(cls, ordered_dict: OrderedDict) -> Dict[Any, Any]:
        return json.loads(json.dumps(ordered_dict))
