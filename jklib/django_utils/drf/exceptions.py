"""Exception classes for DRF."""

# Django
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_409_CONFLICT, HTTP_412_PRECONDITION_FAILED


class Conflict(APIException):
    """Classic '409 Conflict HTTP' error."""

    status_code = HTTP_409_CONFLICT
    default_detail = _("A similar object already exists in the database.")
    default_code = "conflict"


class FailedPrecondition(APIException):
    """Classic '412 Precondition Failed' HTTP error."""

    status_code = HTTP_412_PRECONDITION_FAILED
    default_detail = _("One or several preconditions have not been met.")
    default_code = "precondition_failed"
