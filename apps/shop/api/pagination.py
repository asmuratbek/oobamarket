from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ShopLimitPagination(PageNumberPagination):
    page_size = 21
    page_size_query_param = 'page_size'
    max_page_size = 42
