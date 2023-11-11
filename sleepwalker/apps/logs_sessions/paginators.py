from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LogsSessionsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "items"
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            "pagination": {
                "pages": self.page.paginator.num_pages,
                "current": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count
            },
            "data": data
        })
