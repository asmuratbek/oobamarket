from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from drf_multiple_model.views import MultipleModelAPIView
from rest_auth.registration.views import SocialLoginView
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser
)
from rest_framework.views import APIView

from apps.api.v1.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ShopSerializer,
    ShopCreateSerializer,
    CategorySerializer,
    GlobalCategorySerializer,
    SalesSerializer, ShopReviewsSerializer, ShopContactsSerializer, PlaceSerializer, ParentCategorySerializer,
    ProductDetailSerializer, ProductImageSerializer)
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product, ProductImage
from apps.reviews.models import ShopReviews
from apps.shop.models import Shop, Sales, Contacts, Place
from apps.users.models import User
from .pagination import (
    CategoryLimitPagination,
    ProductLimitPagination,
    ShopLimitPagination,
    ShopProductsLimitPagination
)
from .permissions import IsOwnerOrReadOnly, IsUserOwner


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
    permission_classes = (AllowAny,)

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
    serializer_class = ProductSerializer
    pagination_class = CategoryLimitPagination
    flat = True
    filter_backends = (filters.OrderingFilter,)
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        q = self.request.GET.get('q')
        price_from = self.request.GET.get('priceFrom')
        price_to = self.request.GET.get('priceTo')
        category = Category.objects.get(slug=slug)
        if category.get_level() == 0:
            products = Product.objects.filter(
                Q(category__in=category.get_descendants()),
            ).distinct()
        else:
            products = Product.objects.filter(
                Q(category__in=category.get_descendants()),
            )
        if q:
            products = products.filter(
                Q(title__icontains=str(q))
            ).distinct()
        if price_from and price_from != 'NaN':
            products = products.filter(price__gt=int(price_from))
        if price_to and price_to != 'NaN':
            products = products.filter(price__lt=int(price_to))
        queryList = [
            (products, ProductSerializer),
        ]
        return queryList


class GlobalCategoryListApiView(ListAPIView):
    serializer_class = GlobalCategorySerializer
    queryset = GlobalCategory.objects.all()
    filter_backends = (filters.OrderingFilter,)
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)


class GlobalCategoryGetChildrenApiView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        return Category.objects.filter(section__slug=self.kwargs.get('slug'), parent__isnull=True)


class CategoryDetailChildrenApiView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        return Category.objects.filter(parent__slug=self.kwargs.get('slug'), parent__isnull=False)


class GlobalCategoryDetailApiView(MultipleModelAPIView):
    # queryList = [
    #     (Shop.objects.all(), ShopSerializer),
    #     (Product.objects.all(), ProductSerializer),
    # ]
    pagination_class = CategoryLimitPagination
    flat = True
    filter_backends = (filters.OrderingFilter,)
    serializer_class = ProductSerializer
    permission_classes = (AllowAny, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        q = self.request.GET.get('q')
        price_from = self.request.GET.get('priceFrom')
        price_to = self.request.GET.get('priceTo')
        globalcategory = GlobalCategory.objects.get(slug=slug)
        products = Product.objects.filter(category__section=globalcategory)
        if q:
            products = products.filter(
                Q(title__icontains=str(q))
            ).distinct()
        if price_from and price_from != 'NaN':
            products = products.filter(price__gt=int(price_from))
        if price_to and price_to != 'NaN':
            products = products.filter(price__lt=int(price_to))
        queryList = [
            (products, ProductSerializer),
        ]
        return queryList


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'short_description']
    pagination_class = ProductLimitPagination#PageNumberPagination
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        objects = Product.objects.all()

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            objects = Product.objects.filter(
                Q(title__icontains=q)
            ).distinct()
        elif self.request.GET.get('shop'):
            shop = self.request.GET.get('shop')
            objects = Product.objects.filter(shop__slug=shop)
        else:
            objects = Product.objects.all()
        return objects


class ProductDetailApiView(APIView):
    """
    Возвращает продукт, с его картинками
    """
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, slug):
        product = Product.objects.filter(slug=slug).first()
        images = list()
        for image in ProductImage.objects.filter(product__slug=slug):
            images.append({
                "image": image.image.url
            })
        return JsonResponse({
            "title": product.title,
            "short_description": product.short_description,
            "shop": product.get_shop_title(),
            "price": product.get_price(),
            "images": images,
            "is_favorite": product.favorite.filter(user=self.request.user).exists() if self.request.user.is_authenticated else 0,
            "is_in_cart": True
        })


class ProductUpdateApiView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = (SessionAuthentication, TokenAuthentication)


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
    pagination_class = ShopProductsLimitPagination
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        shops = Shop.objects.all()

        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            shops = shops.filter(
                Q(title__icontains=q)
            ).distinct()
        if self.request.GET.get('place'):
            place = self.request.GET.get('place')
            shops = shops.filter(contacts__place_id=place).distinct()
        return shops


class PlaceListView(ListAPIView):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all().order_by('title')
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)


class ShopDetailApiView(MultipleModelAPIView):
    pagination_class = ShopLimitPagination
    flat = True
    filter_backends = (filters.OrderingFilter,)
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        q = self.request.GET.get('q')
        price_from = self.request.GET.get('priceFrom')
        price_to = self.request.GET.get('priceTo')
        category = self.request.GET.get('category')
        shop = Shop.objects.filter(slug=slug)
        products = Product.objects.filter(shop=shop)
        if category:
            products = products.filter(
                Q(category_id=int(category))
            )
        if q:
            products = products.filter(
                Q(title__icontains=str(q))
            ).distinct()
        if price_from and price_from != 'NaN':
            products = products.filter(price__gt=int(price_from))
        if price_to and price_to != 'NaN':
            products = products.filter(price__lt=int(price_to))
        queryList = [
            (products, ProductSerializer),
        ]
        return queryList


class ShopApiView(MultipleModelAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        queryList = [
            (shop, ShopSerializer),
            (shop.first().get_parent_categories_of_used(), ParentCategorySerializer),
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


class UserShopsListView(ListAPIView):
    """
       Возвращает все Магазины пользователя
    """
    serializer_class = ShopSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = ShopProductsLimitPagination
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = User.objects.filter(id=user_id)
        shops = Shop.objects.filter(user=user)
        return shops


class UserDetailView(APIView):
    permission_classes = (IsUserOwner,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)

        return JsonResponse({
            "status": "success",
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,
            "cart_count": user.get_cart_count(),
            "favorites_count": user.get_favorites_count()
        })


class UserCartItemsView(APIView):
    permission_classes = (IsUserOwner,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        cartitems = list()

        for item in user.cart_set.last().cartitem_set.all():
            cartitems.append({
                "title": item.product.title,
                "short_description": item.product.short_description,
                "shop": item.product.get_shop_title(),
                "price": item.product.get_price(),
                "image": item.product.get_main_thumb_image(),
                "is_favorite": item.product.favorite.filter(user=user).exists(),
                "is_in_cart": True
            })

        return JsonResponse({
            "status": "success",
            "items": cartitems
        })


class UserFavoritesView(APIView):
    permission_classes = (IsUserOwner,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        favorites = list()

        for item in user.get_favorites():
            favorites.append({
                "title": item.product.title,
                "short_description": item.product.short_description,
                "shop": item.product.get_shop_title(),
                "price": item.product.get_price(),
                "image": item.product.get_main_thumb_image(),
                "is_favorite": item.product.favorite.filter(user=user).exists(),
                "is_in_cart": True
            })

        return JsonResponse({
            "status": "success",
            "items": favorites
        })


class ShopDetailView(MultipleModelAPIView):
    """
    Возвращает поля Магазина и его Товары
    """

    filter_backends = (filters.OrderingFilter,)
    serializer_class = ShopSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        products = Product.objects.filter(shop=shop)
        queryList = [
            (shop, ShopSerializer),
            (products, ProductSerializer),
        ]
        return queryList

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(ShopDetailView, self).dispatch(*args, **kwargs)


class ShopSalesView(ListAPIView):
    """
    Возвращает поля Магазина и его Акции
    """
    serializer_class = SalesSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = ShopProductsLimitPagination
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        sales = Sales.objects.filter(shop=shop)
        return sales


class ShopReviewsView(ListAPIView):
    """
    Возвращает поля Магазина и его Отзывы
    """
    serializer_class = ShopReviewsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = ShopProductsLimitPagination
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        reviews = ShopReviews.objects.filter(shop=shop)
        return reviews


class ShopContactsView(ListAPIView):
    """
    Возвращает поля Магазина и его Контакты
    """
    serializer_class = ShopContactsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = ShopProductsLimitPagination
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        shop = Shop.objects.filter(slug=slug)
        contacts = Contacts.objects.filter(shop=shop)
        return contacts
