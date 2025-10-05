from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20  # 20 messages per page
    page_size_query_param = "page_size"  # allow clients to override
    max_page_size = 100
