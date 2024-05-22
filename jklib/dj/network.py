from django.conf import settings
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    """Gets the client IP address from the request."""
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META.get("HTTP_X_FORWARDED_FOR").split(",")[-1].strip()
    elif request.META.get("HTTP_X_REAL_IP"):
        return request.META.get("HTTP_X_REAL_IP")
    return request.META.get("REMOTE_ADDR")


def get_server_domain() -> str:
    """Gets the server domain from the settings."""
    hosts = settings.ALLOWED_HOSTS
    domain = hosts[0] if hosts else "http://127.0.0.1:8000/"
    return domain
