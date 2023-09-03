import logging

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status as rest_status

logger = logging.getLogger(__name__)


def get_api_response(data, message="Ok", status=rest_status.HTTP_200_OK):
    return Response(data, status=status)


class MailboxPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'data': data,
            'num_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'max_page_size': self.max_page_size
        }
