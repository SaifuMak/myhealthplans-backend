
from rest_framework.pagination import PageNumberPagination

class PolicyPagination(PageNumberPagination):
    page_size = 10

