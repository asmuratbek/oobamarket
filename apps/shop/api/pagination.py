from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ShopLimitPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10
