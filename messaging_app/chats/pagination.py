
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    # The API will fetch 20 messages per page by default
    page_size = 20
    # Allows client to specify page number: ?page=X
    page_query_param = 'page'
    # Allows client to override page size: ?page_size=X, with a max of 100
    page_size_query_param = 'page_size'
    max_page_size = 100
    # You can also customize the response format if needed