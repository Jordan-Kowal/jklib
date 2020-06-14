"""
Contains useful function for network management
Functions:
    build_url: Builds a complete URL using the current host, a relative URL, and GET params
    get_client_ip: Returns the IP address of the current user
    get_server_domain: Returns the server domain/url
"""


# Built-in
from urllib.parse import urljoin

# Local
from .utils import get_config


# --------------------------------------------------------------------------------
# > Content
# --------------------------------------------------------------------------------
def build_url(relative_url, params):
    """
    Builds a complete URL using the current host, a relative URL, and GET params
    Args:
        relative_url (str): Relative URL, usually from the reverse() function
        params (dict): Contains list of GET parameters
    Returns:
        (str) The complete URL
    """
    domain = get_server_domain()
    if len(params) > 0:
        serialized_params = "?"
        for key, value in params.items():
            serialized_params += f"{key}={value}&"
        serialized_params = serialized_params[:-1]
        relative_url += serialized_params
    complete_url = urljoin(domain, relative_url)
    return complete_url


def get_client_ip(request):
    """
    Returns the IP address of the current user
    Based on the environment, the address can be different thing: FORWARDED_FOR, REAL_IP, REMOTE_ADDR
    Args:
        request (HttpRequest): HttpRequest from django
    Returns:
        (str) The IP address as string
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
    """Returns the server domain/url"""
    hosts = get_config("ALLOWED_HOSTS")
    domain = hosts[0] if hosts else "http://127.0.0.1:8000/"
    return domain
