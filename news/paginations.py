from rest_framework import pagination


class NewsNumberPagination(pagination.PageNumberPagination):
    page_size = 3
    max_page_size = 100
