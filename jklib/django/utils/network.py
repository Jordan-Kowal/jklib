"""Functions for network management within django"""


# Local
from .settings import get_config


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def build_url_with_params(url, params):
    """
    Builds a complete URL using the current host, a relative URL, and GET params
    :param str url: Main URL without params
    :param dict params: The GET params for the url
    :return: The computed URL
    :rtype: str
    """
    # Exit if no params
    if len(params) == 0:
        return url
    # Format params
    serialized_params = "?"
    for key, value in params.items():
        serialized_params += f"{key}={value}&"
    serialized_params = serialized_params[:-1]
    # Remove extra "/"
    if url[-1] == "/":
        url = url[:-1]
    complete_url = f"{url}{serialized_params}"
    return complete_url


def get_client_ip(request):
    """
    Returns the IP address of the current user
    Based on the environment, the address can be different thing: FORWARDED_FOR, REAL_IP, REMOTE_ADDR
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
