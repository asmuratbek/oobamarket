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
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from apps.category.api.serializers import CategorySerializer
from apps.category.models import Category
from apps.product.api.serializers import ProductSerializer
from apps.product.models import Product
from .pagination import ShopLimitPagination
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from apps.shop.models import Shop
from .serializers import ShopSerializer, ShopCreateSerializer
from drf_multiple_model.views import MultipleModelAPIView


class ShopListApiView(ListAPIView):
    serializer_class = ShopSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    # pagination_class = ShopLimitPagination#PageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        objects = Shop.objects.all()

        if self.request.GET.get('search'):
            q = self.request.GET.get('search')
            objects = Shop.objects.filter(
                Q(title__icontains=q)|
                Q(text__icontains=q)
            ).distinct()
            return objects
        else:
            objects = Shop.objects.all()
            return objects


# class ShopDetailApiView(RetrieveAPIView):
#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer
#     lookup_field = 'slug'
#     permission_classes = [AllowAny]

class ShopDetailApiView(MultipleModelAPIView):
    # queryList = [
    #     (Shop.objects.all(), ShopSerializer),
    #     (Product.objects.all(), ProductSerializer),
    # ]
    pagination_class = ShopLimitPagination
    flat = True

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        queryList = [
            # (shop, ShopSerializer),
            (Product.objects.filter(shop=shop), ProductSerializer),
            # (shop.first().get_used_categories(), CategorySerializer)
        ]
        return queryList


class ShopApiView(MultipleModelAPIView):

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        queryList = [
            (shop, ShopSerializer),
            (shop.first().get_used_categories(), CategorySerializer)
        ]
        return queryList



class ShopUpdateApiView(RetrieveUpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ShopDeleteApiView(DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class ShopCreateApiView(CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
