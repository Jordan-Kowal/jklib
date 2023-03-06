# Django
from rest_framework.pagination import PageNumberPagination


class BasicPagination(PageNumberPagination):
    page_query_param = "page"
    last_page_strings = ["last"]
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 200
