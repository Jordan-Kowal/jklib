"""Pagination classes for DRF."""


# Django
from rest_framework.pagination import PageNumberPagination


class BasicPagination(PageNumberPagination):
    """Basic pagination handler used in common API."""

    # Page navigation
    page_query_param = "page"
    last_page_strings = [
        "last",
    ]
    # Page size
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 200
