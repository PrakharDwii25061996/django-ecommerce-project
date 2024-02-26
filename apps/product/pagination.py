from rest_framework import pagination
from rest_framework.response import Response


class ProductListPagination(pagination.PageNumberPagination):

    page_size = 3  # Number of items per page
    page_size_query_param = 'page'  # Custom query parameter for changing page size
    max_page_size = 5  # Maximum number of items per page

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
