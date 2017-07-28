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
from apps.global_category.models import GlobalCategory
from .serializers import GlobalCategorySerializer


class GlobalCategoryListApiView(ListAPIView):
    serializer_class = GlobalCategorySerializer
    # pagination_class = ShopLimitPagination#PageNumberPagination
    queryset = GlobalCategory.objects.all()


class GlobalCategoryDetailApiView(MultipleModelAPIView):
    # queryList = [
    #     (Shop.objects.all(), ShopSerializer),
    #     (Product.objects.all(), ProductSerializer),
    # ]

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        globalcategory = GlobalCategory.objects.get(slug=slug)
        queryList = [
            (Product.objects.filter(category__section=globalcategory), ProductSerializer),
        ]
        return queryList
