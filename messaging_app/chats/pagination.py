from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    # The API will fetch 20 messages per page by default
    page_size = 20
    # Allows client to specify page number: ?page=X
    page_query_param = 'page'
    # Allows client to override page size: ?page_size=X, with a max of 100
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Customize the response to include page.paginator.count
        return Response({
            'count': self.page.paginator.count,  # Total number of items
            'next': self.get_next_link(),        # URL to next page
            'previous': self.get_previous_link(), # URL to previous page
            'results': data                      # Paginated data
        })
