# pagination.py
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # default
    page_size_query_param = 'size'  # client can use ?size=20
    max_page_size = 100  # optional limit
