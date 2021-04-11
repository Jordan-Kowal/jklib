"""Functions for network management within django"""

# Built-in
from urllib.parse import urlencode

# Local
from .settings import get_config


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def build_url(parts, params=None, end_slash=False):
    """
    Builds a complete URL by joining its parts and adding params at the end
    :param list parts: Ordered list of paths to join
    :param dict params: The GET params for the url
    :param bool end_slash: Whether we should add a / at the end
    :return: The computed URL
    :rtype: str
    """
    # Remove extra slashes
    cleaned_parts = []
    for part in parts:
        if part == "":
            continue
        if part[0] == "/":
            part = part[1:]
        if part[-1] == "/":
            part = part[:-1]
        cleaned_parts.append(part)
    # Build URL
    url = "/".join(cleaned_parts)
    if params is not None:
        url += urlencode(params)
    if end_slash:
        url += "/"
    return url.replace("//", "/")


def get_client_ip(request):
    """
    Extract the IP address from the request (either from FORWARDED_FOR, REAL_IP, or REMOTE_ADDR)
    :param request: HttpRequest from django
    :return: The user's IP address
    :rtype: str
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # FORWARDED_FOR
        ip = x_forwarded_for.split(",")[-1].strip()
    elif request.META.get("HTTP_X_REAL_IP"):
        # REAL_IP
        ip = request.META.get("HTTP_X_REAL_IP")
    else:
        # REMOTE_ADDR
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_server_domain():
    """
    Fetches the django server address from the settings
    :return: The server domain/url
    :rtype: str
    """
    hosts = get_config("ALLOWED_HOSTS")
    domain = hosts[0] if hosts else "http://127.0.0.1:8000/"
    return domain
