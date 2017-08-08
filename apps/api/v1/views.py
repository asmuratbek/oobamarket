from django.db.models import Q
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

from apps.api.v1.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ShopSerializer,
    ShopCreateSerializer,
    CategorySerializer,
    GlobalCategorySerializer
)

from apps.product.models import Product
from apps.shop.models import Shop
from .pagination import (
    CategoryLimitPagination,
    ProductLimitPagination,
    ShopLimitPagination
)

from .permissions import IsOwnerOrReadOnly
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    # pagination_class = ShopLimitPagination#PageNumberPagination
    queryset = Category.objects.all()


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
    pagination_class = CategoryLimitPagination
    flat = True

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        category = Category.objects.get(slug=slug)
        queryList = [
            (Product.objects.filter(category=category), ProductSerializer),
        ]
        return queryList


class GlobalCategoryListApiView(ListAPIView):
    serializer_class = GlobalCategorySerializer
    queryset = GlobalCategory.objects.all()


class GlobalCategoryDetailApiView(MultipleModelAPIView):
    # queryList = [
    #     (Shop.objects.all(), ShopSerializer),
    #     (Product.objects.all(), ProductSerializer),
    # ]
    pagination_class = CategoryLimitPagination
    flat = True

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        globalcategory = GlobalCategory.objects.get(slug=slug)
        queryList = [
            (Product.objects.filter(category__section=globalcategory), ProductSerializer),
        ]
        return queryList


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'short_description']
    pagination_class = ProductLimitPagination#PageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        objects = Product.objects.all()

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            print(q)
            objects = Product.objects.filter(
                Q(title__icontains=q)|
                Q(short_description__icontains=q)
            ).distinct()
            print(objects)
        elif self.request.GET.get('shop'):
            shop = self.request.GET.get('shop')
            objects = Product.objects.filter(shop__slug=shop)
        else:
            objects = Product.objects.all()
        return objects


class ProductDetailApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class ProductUpdateApiView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

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
