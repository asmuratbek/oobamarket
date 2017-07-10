from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CategoryLimitPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10
