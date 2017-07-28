from django.shortcuts import get_object_or_404
from drf_multiple_model.views import MultipleModelAPIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from apps.product.api.serializers import ProductSerializer
from apps.product.models import Product
from apps.shop.models import Shop
from .pagination import CategoryLimitPagination
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from apps.category.models import Category
from .serializers import CategorySerializer


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    # pagination_class = ShopLimitPagination#PageNumberPagination
    queryset = Category.objects.all()


# class CategoryDetailApiView(RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_field = 'slug'
#     permission_classes = [AllowAny]


class GetUsedCategoriesFromShop(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        shop = get_object_or_404(Shop, slug=slug)
        objects = shop.get_used_categories()
        return objects


class CategoryDetailApiView(MultipleModelAPIView):
    # queryList = [
    #     (Shop.objects.all(), ShopSerializer),
    #     (Product.objects.all(), ProductSerializer),
    # ]

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        category = Category.objects.get(slug=slug)
        queryList = [
            (Product.objects.filter(category=category), ProductSerializer),
        ]
        return queryList
