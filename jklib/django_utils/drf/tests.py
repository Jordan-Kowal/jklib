"""Useful constants, functions, and classes for test management in DRF."""
# Built-in
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union
from urllib.parse import urlencode
from zipfile import ZipFile

# Django
from django.contrib.sessions.models import Session
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.test import APIClient

# Local
from ..utils.tests import ImprovedTestCase

if TYPE_CHECKING:
    # Django
    from django.contrib.auth.models import User as UserType

CONTENT_DISPOSITION = 'attachment; filename="{file_name}"'


class ActionTestCase(ImprovedTestCase):
    """TestCase that provides utility for testing DRF actions/endpoints."""

    viewset_url: str = ""
    api_client_class: Type[APIClient] = APIClient
    api_client: APIClient
    payload: Dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up the API client."""
        cls.api_client = cls.api_client_class()
        super().setUpClass()

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

    def assertDownloadFile(self, url: str, file_name: str) -> None:
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            CONTENT_DISPOSITION.format(file_name=file_name),
        )

    def assertDownloadZipFile(
        self, url: str, file_name: str, zip_content: List[str]
    ) -> None:
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            CONTENT_DISPOSITION.format(file_name=file_name),
        )
        # Check the zip content
        myzip = ZipFile(BytesIO(response.getvalue()))
        zipped_files = set(myzip.namelist())
        self.assertSetEqual(set(zip_content), zipped_files)

    def build_url(
        self,
        extra_path: str = None,
        detail_key: Union[str, int] = None,
        params: Optional[Dict] = None,
    ) -> str:
        url = self.viewset_url
        if detail_key is not None:
            url = f"{url}{detail_key}/"
        if extra_path is not None:
            url = f"{url}{extra_path}/"
        if params is not None:
            if url[-1] != "/":
                url += "/"
            url += f"?{urlencode(params)}"
            return url.replace("//", "/")
        if url[-1] != "/":
            url += "/"
        if url[0] != "/":
            url = "/" + url
        return url.replace("//", "/")

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
        flat_dict = self._dict_to_flat_dict(payload)
        data = encode_multipart(data=flat_dict, boundary=BOUNDARY)
        method = getattr(self.api_client, method.lower())
        return method(url, data=data, content_type=MULTIPART_CONTENT, *args, **kwargs)

    @staticmethod
    def _dict_to_flat_dict(data: Dict[str, Any]) -> Dict[str, Union[str, int, bool]]:
        """Recursively flattens a dict so that all of its keys are at the first
        level.

        Keys for nested arrays or dicts might look like
        'key[0][subkey][3]'
        """
        flat_dict = {}

        def _convert_value(current_path: str, current_value: Any) -> None:
            # Undefined values are skipped
            if current_value is None or current_value == "":
                return
            # Array: Add index to path for each value and recurse
            if type(current_value) == list:
                for i, sub_value in enumerate(current_value):
                    new_path = f"{current_path}[{i}]"
                    _convert_value(new_path, sub_value)
                return
            # Object: Add key to path for each value and recurse
            if type(current_value) == dict:
                for sub_key, sub_value in current_value.items():
                    new_path = f"{current_path}[{str(sub_key)}]"
                    _convert_value(new_path, sub_value)
                return
            # All other cases: Set value
            flat_dict[current_path] = current_value

        for key, value in data.items():
            _convert_value(str(key), value)
        return flat_dict
