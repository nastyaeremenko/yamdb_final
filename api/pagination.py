from rest_framework.pagination import PageNumberPagination


class ReviewPagePagination(PageNumberPagination):
    page_size = 1
