# Built-in
import datetime
from io import BytesIO
from typing import (
    TYPE_CHECKING,
    Any,
    ByteString,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    Union,
)
from urllib.parse import urlencode
from zipfile import ZipFile

# Django
from django.contrib.sessions.models import Session
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models import FileField, ImageField, Model, QuerySet
from django.test import RequestFactory, TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient

# Application
from jklib.std.images import image_to_base64, resized_image_to_base64
from jklib.std.transforms import dict_to_flat_dict

if TYPE_CHECKING:
    # Django
    from django.contrib.auth.models import User as UserType

CONTENT_DISPOSITION = 'attachment; filename="{file_name}"'


def assert_logs(logger: str, level: str) -> Callable:
    """Wraps a test into a `self.assertLogs`."""
    level = level.upper()

    def decorator(function: Callable) -> Callable:
        def wrapper(self: TestCase, *args, **kwargs) -> Any:
            with self.assertLogs(logger=logger, level=level) as context:
                self.logger_context = context
                return function(self, *args, **kwargs)

        return wrapper

    return decorator


class AssertionTestCase(TestCase):
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

    def assertDownloadFile(self, response: Response, file_name: str) -> None:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            CONTENT_DISPOSITION.format(file_name=file_name),
        )

    def assertDownloadZipFile(
        self, response: Response, file_name: str, zip_content: List[str]
    ) -> None:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            CONTENT_DISPOSITION.format(file_name=file_name),
        )
        # Check the zip content
        myzip = ZipFile(BytesIO(response.getvalue()))
        zipped_files = set(myzip.namelist())
        self.assertSetEqual(set(zip_content), zipped_files)

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

    def assertFieldsHaveError(
        self,
        response: Response,
        key_paths: List[str],
    ) -> None:
        self.assertEqual(response.status_code, 400)
        for key_path in key_paths:
            # key_path example: "valves.0.description"
            value = response.data
            for key in key_path.split("."):
                if isinstance(value, list):
                    value = value[int(key)]
                else:
                    value = value.get(key)
            self.assertIsNotNone(value)

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

    def assertFileIsNone(self, file_field: FileField) -> None:
        self.assertFalse(bool(file_field))

    def assertImageToBase64(
        self, img: ImageField, data: ByteString, resize_to: Optional[int] = None
    ):
        converted_image = (
            resized_image_to_base64(img, resize_to)
            if resize_to is not None
            else image_to_base64(img)
        )
        self.assertEqual(converted_image, data)

    def assertIntegrityErrorOnSave(self, instance: Model) -> None:
        with self.assertRaises(IntegrityError):
            instance.save()

    def assertQuerySetPks(
        self, queryset: QuerySet, expected_pks=Iterable[Any], pk="id"
    ) -> None:
        queryset_pks = {getattr(item, pk) for item in queryset}
        self.assertSetEqual(queryset_pks, set(expected_pks))


class ImprovedTestCase(AssertionTestCase):
    @staticmethod
    def build_fake_request(
        method: str = "get", path: str = "/", data: Dict = None
    ) -> Request:
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
        if upload_name is None:
            upload_name = filepath.split("/")[-1]
        with open(filepath, "rb") as f:
            binary_content = f.read()
        return SimpleUploadedFile(
            name=upload_name,
            content=binary_content,
        )


class APITestCase(ImprovedTestCase):
    viewset_url: str = ""
    api_client_class: Type[APIClient] = APIClient
    api_client: APIClient
    payload: Dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.api_client = cls.api_client_class()
        super().setUpClass()

    def build_url(
        self,
        extra_path: str = None,
        detail_key: Union[str, int] = None,
        params: Optional[Dict] = None,
    ) -> str:
        url = self.viewset_url
        if url[-1] != "/":
            url += "/"
        if detail_key is not None:
            url += f"{detail_key}/"
        if extra_path is not None:
            url += f"{extra_path}/"
        if params is not None:
            url += f"?{urlencode(params)}"
        return url

    @staticmethod
    def disconnect_user(user: "UserType") -> None:
        """Removes all active sessions for the user."""
        user_active_session_ids = []
        all_active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in all_active_sessions:
            if session.get_decoded().get("_auth_user_id") == str(user.pk):
                user_active_session_ids.append(session.pk)
        if len(user_active_session_ids) > 0:
            Session.objects.filter(pk__in=user_active_session_ids).delete()

    def multipart_api_call(
        self,
        method: str,
        url: str,
        payload: Dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Transforms a JSON payload into a flattened form-data and performs a
        multipart request."""
        flat_dict = dict_to_flat_dict(payload)
        data = encode_multipart(data=flat_dict, boundary=BOUNDARY)
        method = getattr(self.api_client, method.lower())
        return method(url, data=data, content_type=MULTIPART_CONTENT, *args, **kwargs)
