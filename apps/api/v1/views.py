import uuid
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialToken, SocialLogin
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from braces.views import CsrfExemptMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django import db
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_multiple_model.views import MultipleModelAPIView
from rest_auth.registration.views import SocialLoginView
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
from rest_framework.parsers import FormParser, FileUploadParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated)
from rest_framework.views import APIView
from slugify import slugify
from django.forms.models import model_to_dict
from apps.api.v1.serializers import *
from apps.api.v1.social_auth import SocialAuth
from apps.cart.models import Cart, CartItem
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product, ProductImage, FavoriteProduct
from apps.shop.models import Shop, Contacts, Place
from apps.users.models import User, Subscription
from apps.utils.views import send_letters_to_shop
from .pagination import (
    CategoryLimitPagination,
    ProductLimitPagination,
    ShopLimitPagination,
    ShopProductsLimitPagination
)
from .permissions import *
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.postgres.search import TrigramSimilarity

from requests.exceptions import HTTPError

ORDER_TYPES = ["price", "-price", "title", "created_at"]


class FacebookLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        social_auth = SocialAuth(token_key='social_token', provider='facebook')
        return social_auth.login(request)


class GoogleLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        social_auth = SocialAuth(token_key='social_token', provider='google')
        return social_auth.login(request)


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    # pagination_class = ShopLimitPagination#PageNumberPagination
    queryset = Category.objects.all()


class ProductAddToFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, slug):
        favorite = FavoriteProduct.objects.filter(product__slug=slug, user=request.user)
        if favorite:
            favorite.first().delete()
            status = "success"
            message = "deleted from favorite"
        else:
            product = get_object_or_404(Product, slug=slug)
            favorite = FavoriteProduct(product=product, user=request.user)
            favorite.save()
            # FavoriteProduct.objects.create(product=product)
            status = "success"
            message = "added to favorites list"
        return JsonResponse({
            "status": status,
            "message": message
        })


class LentaView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        sub_list = list()
        for sub in user.subscription_set.all():
            if sub.subscription_type == 'only_actions':
                [sub_list.append(item) for item in sub.subscription.sales_set.all().order_by("created_at")]
            elif sub.subscription_type == 'only_products':
                [sub_list.append(item) for item in sub.subscription.product_set.all().order_by("created_at")]
            else:
                [sub_list.append(item) for item in sub.subscription.sales_set.all().order_by("created_at")]
                [sub_list.append(item) for item in sub.subscription.product_set.all().order_by("created_at")]
        sorted_list = sorted(sub_list, key=lambda x: x.created_at, reverse=True)
        paginator = Paginator(sorted_list, 10)
        page = self.request.GET.get('page', 1)
        try:
            p = paginator.page(int(page))
        except (EmptyPage, ValueError):
            p = None
        items = list()
        if p:
            for item in p.object_list:
                if item.__class__.__name__ == "Product":
                    items.append({
                        "title": item.title,
                        "type": "product",
                        "slug": item.slug,
                        "short_description": item.short_description,
                        "shop": item.get_shop_title(),
                        "shop_logo": item.shop.logo_thumb.url if item.shop.logo_thumb else None,
                        "main_image": item.get_main_thumb_image(),
                        "price": item.get_price(),
                        "is_favorite": item.favorite.filter(user=user).exists(),
                        "is_in_cart": user.cart_set.last().cartitem_set.filter(product=item).exists() \
                            if user.cart_set.all() else False
                    })
                else:
                    items.append(dict(shop=item.shop.title, title=item.title, short_description=item.short_description,
                                      description=item.description, discount=item.discount, id=item.id,
                                      shop_logo=item.shop.logo_thumb.url if item.shop.logo_thumb else None, main_image=item.image.url if item.image else None,
                                      type="sale"))
        return JsonResponse({
            "status": "success",
            "page": page if page else 1,
            "items": items,
            "count": paginator.count
        })


class ProductAddToCartView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, slug):
        cart = Cart.objects.filter(user=request.user).last()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product__slug=slug)
        if cart_item:
            cart_item.first().delete()
            status = "success"
            message = "removed from cart"
        else:
            product = get_object_or_404(Product, slug=slug)
            cart_item = CartItem(cart=cart, product=product)
            cart_item.save()
            status = "success"
            message = "added to cart"
        return JsonResponse({
            "status": status,
            "message": message
        })


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
        order = self.request.GET.get('order')
        price_from = self.request.GET.get('priceFrom')
        price_to = self.request.GET.get('priceTo')
        category = get_object_or_404(Category, slug=slug)
        if category.get_level() == 0:
            if order and order in ORDER_TYPES:
                products = Product.objects.filter(
                    Q(category__in=category.get_descendants()),
                ).order_by(order).distinct()
            else:
                products = Product.objects.filter(
                    Q(category__in=category.get_descendants()),
                ).distinct()
        else:
            if order and order in ORDER_TYPES:
                products = Product.objects.filter(
                    Q(category=category),
                ).order_by(order)
            else:
                products = Product.objects.filter(
                    Q(category=category),
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
    queryset = GlobalCategory.objects.filter(hidden=False)
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


class GlobalCategoryDetailApiView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        q = self.request.GET.get('q')
        order = self.request.GET.get('order')
        price_from = self.request.GET.get('priceFrom')
        price_to = self.request.GET.get('priceTo')
        globalcategory = GlobalCategory.objects.get(slug=slug)
        if order and order in ORDER_TYPES:
            products = Product.objects.filter(category__section=globalcategory).order_by(order)
        else:
            products = Product.objects.filter(category__section=globalcategory)
        if q:
            products = products.filter(
                Q(title__icontains=str(q))
            ).distinct()
        if price_from and price_from != 'NaN':
            products = products.filter(price__gt=int(price_from))
        if price_to and price_to != 'NaN':
            products = products.filter(price__lt=int(price_to))
        paginator = Paginator(products, 20)
        page = request.GET.get('page', 1)
        try:
            p = paginator.page(int(page))
        except (AttributeError, EmptyPage, ValueError):
            p = None
        product_list = list()
        if p:
            for product in p.object_list:
                product_list.append({
                    "title": product.title,
                    "slug": product.slug,
                    "short_description": product.short_description,
                    "shop": product.get_shop_title(),
                    "main_image": product.get_main_thumb_image(),
                    "price": product.get_price(),
                    "is_favorite": product.favorite.filter(
                        user=self.request.user).exists() if self.request.user.is_authenticated else False,
                    "is_in_cart": self.request.user.cart_set.last().cartitem_set.filter(product=product).exists() \
                        if self.request.user.is_authenticated \
                           and self.request.user.cart_set.all() \
                        else False
                })

        return JsonResponse({
            "status": "success",
            "page": page,
            "products": product_list
        })


class MyListView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):
        cart = request.user.cart_set.last()
        cart_items = cart.cartitem_set.all().values("product__id") \
            if request.user.is_authenticated and cart is not None else False
        items = list()
        favs = list()
        shop_titles = list()
        if cart_items:
            for item in cart_items:
                items.append({
                    "id": item.get("product__id")
                })
        favorites = request.user.favoriteproduct_set.all() \
            if request.user.is_authenticated and request.user.favoriteproduct_set else False
        if favorites:
            for fav in favorites:
                favs.append({
                    "id": fav.product.id
                })
        shops = request.user.shop_titles() if request.user.is_authenticated and request.user.shop_set else False
        if shops:
            for shop in shops:
                shop_titles.append({
                    "title": shop.get("title")
                })
        return JsonResponse({
            "favorites": favs if favs else [],
            "cart_items": items if items else [],
            "shops": shop_titles if shop_titles else [],
            "isAuth": request.user.is_authenticated()
        })


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'short_description']
    pagination_class = ProductLimitPagination  # PageNumberPagination
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
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        product = Product.objects.filter(slug=slug).first()
        images = list()
        user = request.user
        user_cart = user.cart_set.last() if user.is_authenticated() else None
        products_in_cart = [item.product for item in user_cart.cartitem_set.all()] if user_cart else None
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
            "is_favorite": product.favorite.filter(
                user=self.request.user).exists() if self.request.user.is_authenticated else 0,
            "is_in_cart": True if products_in_cart and product in products_in_cart else False,
            "url": product.get_absolute_url()
        })


class ProductUpdateApiView(CsrfExemptMixin, APIView):
    queryset = Product.objects.all()
    serializer_class = ProductPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerShop4Product]
    authentication_classes = (TokenAuthentication, )

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        product_images = [{'image_id': i.id, 'image_url': i.image.url}
                          for i in product.productimage_set.all()]
        product_dict = model_to_dict(product, exclude=['shop', 'category'])
        product_dict['shop'] = dict(id=product.shop.id, title=product.shop.title, slug=product.shop.slug)
        product_dict['global_category'] = dict(id=product.category.parent.section.id,
                                               title=product.category.parent.section.title,
                                               slug=product.category.parent.section.slug)
        product_dict['parent_category'] = dict(id=product.category.parent.id, title=product.category.parent.title,
                                               slug=product.category.parent.slug)
        product_dict['category'] = dict(id=product.category.id, title=product.category.title,
                                        slug=product.category.slug)
        return JsonResponse(dict(images=product_images, product=product_dict))

    def post(self, *args, **kwargs):
        product = get_object_or_404(klass=Product, slug=kwargs['slug'])
        product_serializer = ProductPostSerializer(product, data=self.request.data)

        if product_serializer.is_valid():
            product_serializer.save(category=get_object_or_404(Category, slug=self.request.POST.get('category', '')),
                                    shop=get_object_or_404(Shop, slug=self.request.POST.get('shop', '')))

            images_files = self.request.FILES.getlist('images_files', '')
            remove_images_list = [int(i) for i in self.request.data.getlist('delete_images', [])
                                  if i not in ['', None]]

            ProductImage.objects.filter(id__in=remove_images_list).delete()

            if images_files:
                image_list = [ProductImage(product=product, image=img) for img in images_files]
                ProductImage.objects.bulk_create(image_list)
            return JsonResponse({'status': 0, 'message': 'Product is successfully updated.'})
        else:
            return JsonResponse(dict(status=1, message='Product data is invalid'), status=400)


class ProductDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOfProduct]
    authentication_classes = [TokenAuthentication]

    def post(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs.get('slug'))
        product.delete()
        return JsonResponse({'status': 0, 'message': 'Product is successfully deleted.'})


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerShop4Product,)

    def perform_create(self, serializer):
        product = serializer.save(shop=get_object_or_404(Shop, slug=self.request.data.get('shop', '')),
                                  category=get_object_or_404(Category, slug=self.request.data.get('category', '')),
                                  slug=str(slugify(self.request.data.get("title", ""))) + "-" + str(uuid.uuid4())[:4])
        images_files = self.request.FILES.getlist('images_files', '')
        if images_files:
            image_list = [ProductImage(product=product, image=img) for img in images_files]
            ProductImage.objects.bulk_create(image_list)
        return JsonResponse({'status': 0, 'message': 'Product is successfully created.'})


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
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get_queryList(self):
        slug = self.kwargs.get('slug')
        q = self.request.GET.get('q')
        order = self.request.GET.get('order')
        price_from = self.request.GET.get('priceFrom')
        price_to = self.request.GET.get('priceTo')
        category = self.request.GET.get('category')
        shop = Shop.objects.filter(slug=slug)
        if order and order in ORDER_TYPES:
            products = Product.objects.filter(shop=shop).order_by(order)
        else:
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
            (products, ProductDetailSerializer),
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


class ShopApiMobileView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        is_authenticated = request.user.is_authenticated
        return JsonResponse({
            "title": shop.title,
            "slug": shop.slug,
            "email": shop.email,
            "short_description": shop.short_description,
            "description": shop.description,
            "logo": shop.get_logo(),
            "is_owner": shop.is_owner(request.user) if is_authenticated else False,
            "is_subscribed": request.user.subscription_set.filter(
                subscription=shop).exists() if is_authenticated else False,
        })


class ShopCategoriesApiView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        parent_categories = list()
        for parent_category in shop.get_parent_categories_of_used():
            parent_categories.append({
                "id": parent_category.id,
                "title": parent_category.title,
                "slug": parent_category.slug
            })

        return JsonResponse({
            "status": "success",
            "categories": parent_categories
        })


class ShopSalesView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        sales = list()
        for sale in shop.sales_set.all():
            sales.append({
                "id": sale.id,
                "title": sale.title,
                "short_description": sale.short_description,
                "description": sale.description,
                "discount": sale.discount,
                "image": sale.image_thumb.url if sale.image_thumb else None
            })

        return JsonResponse({
            "status": "success",
            "sales": sales
        })

    def post(self, *args, **kwargs):
        self.permission_classes = [IsOwnerShop4Shop]
        shop = get_object_or_404(Shop, slug=kwargs.get('slug', ''))
        serializer = SalesSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(shop=shop)
            return JsonResponse({'status': 0, 'message': 'Sale is successfully created.'})
        return JsonResponse({'status': 1, 'message': 'Sale values is not valid.'})


class SalesUpdate(CsrfExemptMixin, APIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsOwnerShop4Shop, IsSaleOfShop]
    authentication_classes = (TokenAuthentication, )

    def get(self, *args, **kwargs):
        sale = get_object_or_404(Sales, id=kwargs.get('pk'))
        sale_dict = model_to_dict(sale, exclude=['image', 'image_thumb'])
        sale_dict['image'] = sale.image_thumb.url if sale.image_thumb else None
        return JsonResponse({'status': 0, 'sale': sale_dict})

    def post(self, *args, **kwargs):
        sale = get_object_or_404(Sales, pk=kwargs['pk'])
        sale_serializer = SalesSerializer(sale, data=self.request.data)

        if sale_serializer.is_valid():
            image = self.request.FILES.get('image', None)

            if image:
                sale_serializer.save(image=image)
            else:
                sale_serializer.save()

            return JsonResponse(dict(success=0, message='Sale successfully updated'))
        else:
            return JsonResponse(dict(message='Sale data is invalid'), status=400)


class SaleDelete(APIView):
    permission_classes = [IsAuthenticated, IsOwnerShop4Shop, IsSaleOfShop]
    authentication_classes = (TokenAuthentication, )

    def post(self, *args, **kwargs):
        sale = get_object_or_404(Sales, pk=kwargs.get('pk'))
        sale.delete()
        return JsonResponse({'status': 0, 'message': 'Sale is successfully deleted.'})


class ShopContactsView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        contact = shop.contacts_set.first()
        if contact:
            contact_dict = model_to_dict(contact, exclude=['place', 'latitude', 'longitude', 'shop'])
            contact_dict['latitude'] = contact.place.latitude if contact.place else contact.latitude
            contact_dict['longitude'] = contact.place.longitude if contact.place else contact.longitude
            contact_dict['place'] = contact.place.__str__() if contact.place else None
            return JsonResponse({"status": "success", "contacts": contact_dict})
        return JsonResponse({'status': "success", "contacts": None})


class ShopReviewsView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        reviews = list()
        for review in shop.shopreviews_set.all():
            reviews.append({
                "user": review.user.username if review.user.username else review.user.email,
                "text": review.text,
                "stars": len(review.stars) if review.stars else None
            })

        return JsonResponse({
            "status": "success",
            "reviews": reviews
        })

    def post(self, request, slug):
        self.permission_classes = [IsAuthenticated]
        shop = get_object_or_404(Shop, slug=slug)
        stars_count = request.POST.get("stars")
        if stars_count:
            try:
                if int(stars_count) > 5:
                    stars_count = 5
                elif int(stars_count) < 1:
                    stars_count = 1
                stars = "*" * int(stars_count)
            except (ValueError, TypeError):
                stars = None
        else:
            stars = None
        serializer = ShopReviewsSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save(stars=stars, user=request.user, shop=shop)
            return JsonResponse({'status': 0, 'message': 'Review is successfully created.'})
        else:
            return JsonResponse({'status': 1, 'message': serializer.errors})


class ShopCategoryChildrenApiView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug, category_slug):
        shop = get_object_or_404(Shop, slug=slug)
        category = get_object_or_404(Category, slug=category_slug)
        children = list()
        for child in category.get_children().filter(id__in=shop.get_used_category_ids()):
            children.append({
                "title": child.title,
                "id": child.id,
                "slug": child.slug
            })

        return JsonResponse({
            "status": "success",
            "children": children
        })


class ShopUpdateApiView(CsrfExemptMixin, APIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerShop4Shop]
    authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=kwargs['slug'])
        contact = shop.contacts_set.first()

        shop_dict = model_to_dict(shop, exclude=['logo', 'user', 'logo_thumb'])
        shop_dict['logo'] = shop.logo_thumb.url if shop.logo_thumb else None
        shop_dict['users'] = [user.id for user in shop.user.all()]
        shop_dict['contact'] = model_to_dict(contact) if contact is not None else None
        return JsonResponse(shop_dict)

    def post(self, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=kwargs['slug'])
        shop_serializer = ShopUpdateSerializer(shop, data=self.request.data)

        if shop_serializer.is_valid():
            shop_serializer.save()
            remove_logo = self.request.data.get("remove_logo", 'false')
            new_logo = self.request.FILES.get("new_logo")
            if remove_logo == 'true':
                shop.logo = None
                shop.save()
            if new_logo:
                shop.logo = new_logo
                shop.save()
            contact = shop.contacts_set.first()
            place_id = self.request.data.get("place_id")
            contact_dict = dict(
                phone=self.request.data.get("phone"),
                address=self.request.data.get("address"),
                monday=self.request.data.get("monday"),
                tuesday=self.request.data.get("tuesday"),
                wednesday=self.request.data.get("wednesday"),
                thursday=self.request.data.get("thursday"),
                friday=self.request.data.get("friday"),
                shop=shop,
                saturday=self.request.data.get("saturday"),
                sunday=self.request.data.get("sunday"),
                round_the_clock=self.request.data.get("round_the_clock", False),
                longitude=self.request.data.get("longitude"),
                latitude=self.request.data.get("latitude"),
                place=Place.objects.filter(id=place_id).first())
            are_values = [contact_dict[k] for k in contact_dict.keys()
                          if k != "shop" and contact_dict[k] not in [None, '']]
            if contact:
                contact(**contact_dict)
                contact.save()
            else:
                if are_values:
                    Contacts.objects.create(**contact_dict)

            return JsonResponse(dict(success=0, message='Shop successfully updated'))
        else:
            return JsonResponse(dict(message='Shop data is invalid'), status=400)


class ShopDeleteApiView(DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerShop4Shop]


class ShopCreateApiView(CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        shop = serializer.save(user=[self.request.user.id],
                               slug=str(slugify(self.request.POST.get("title"))) + "-" + str(uuid.uuid4())[:4],
                               published=True)
        place_id = self.request.POST.get("place_id")
        place = Place.objects.filter(id=int(place_id)).first()
        round_the_clock = self.request.POST.get("round_the_clock", False)
        contact_dict = dict(
            phone=self.request.POST.get("phone"),
            address=self.request.POST.get("address"),
            monday=self.request.POST.get("monday"),
            tuesday=self.request.POST.get("tuesday"),
            wednesday=self.request.POST.get("wednesday"),
            thursday=self.request.POST.get("thursday"),
            friday=self.request.POST.get("friday"),
            shop=shop.id,
            saturday=self.request.POST.get("saturday"),
            sunday=self.request.POST.get("sunday"),
            round_the_clock=round_the_clock,
            longitude=self.request.POST.get("longitude"),
            latitude=self.request.POST.get("latitude"),
            place=place.id if place else None)
        are_values = [contact_dict[k] for k in contact_dict.keys()
                      if k != "shop" and contact_dict[k] != None
                      and contact_dict[k] != "" and contact_dict[k] != False]
        if are_values:
            contact = ShopContactsSerializer(data=contact_dict)
            if contact.is_valid():
                contact.save()
            else:
                print(contact.errors)


# class UserShopsListView(ListAPIView):
#     """
#        Возвращает все Магазины пользователя
#     """
#     serializer_class = ShopSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     pagination_class = ShopProductsLimitPagination
#     permission_classes = [AllowAny]
#     authentication_classes = (SessionAuthentication, TokenAuthentication)
#
#     def get_queryset(self):
#         user_id = self.kwargs.get('pk')
#         user = User.objects.filter(id=user_id)
#         shops = Shop.objects.filter(user=user)
#         return shops


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        shops = list()
        for shop in user.shop_set.all():
            shops.append({
                "title": shop.title,
                "slug": shop.slug,
                "logo": shop.get_logo_thumb(),
                "short_description": shop.short_description,
                "email": shop.email
            })

        return JsonResponse({
            "status": "success",
            "shops": shops,
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,
            "cart_count": user.get_cart_count(),
            "favorites_count": user.get_favorites_count()
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 0, 'message': 'User is successfully updated.'})
        return JsonResponse({'status': 1, 'message': serializer.errors})


class UserCartItemsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        cartitems = list()
        for item in user.cart_set.last().cartitem_set.all():
            cartitems.append({
                "title": item.product.title,
                "quantity": item.quantity,
                "slug": item.product.slug,
                "short_description": item.product.short_description,
                "shop": item.product.get_shop_title(),
                "price": item.product.get_price(),
                "total": item.total,
                "image": item.product.get_main_thumb_image(),
                "is_favorite": item.product.favorite.filter(user=user).exists(),
                "is_in_cart": True
            })
        shops = list()
        for index, shop in enumerate(user.cart_set.last().get_shops()):
            items = list()
            for item in cartitems:
                if item.get('shop') == shop.title:
                    items.append(item)
            shops.append({
                "title": shop.title,
                "logo": shop.get_logo_thumb(),
                "items": items,
                "delivery": 150 if index == 0 else 100
            })

        return JsonResponse({
            "status": "success",
            "delivery_total": user.cart_set.last().get_delivery_total(),
            "shops": shops,
            "total": user.cart_set.last().subtotal
        })


class ProductChangeCartView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        user = get_object_or_404(User, id=request.user.id)
        cart = user.cart_set.last()
        quantity = request.POST.get('quantity')
        if cart.cartitem_set.filter(product__slug=slug):
            status = "success"
            cartitem = cart.cartitem_set.filter(product__slug=slug).first()
            cartitem.quantity = quantity
            cartitem.save()
            return JsonResponse({
                "status": status,
                "total": cartitem.total
            })
        else:
            status = "error"
            return JsonResponse({
                "status": status
            })


class UserFavoritesView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        favorites = list()

        for item in user.get_favorites():
            favorites.append({
                "title": item.product.title,
                "slug": item.product.slug,
                "short_description": item.product.short_description,
                "shop": item.product.get_shop_title(),
                "price": item.product.get_price(),
                "image": item.product.get_main_thumb_image(),
                "is_favorite": item.product.favorite.filter(user=user).exists(),
                "is_in_cart": self.request.user.cart_set.last().cartitem_set.filter(product=item.product).exists() \
                    if self.request.user.is_authenticated \
                       and self.request.user.cart_set.all() \
                    else False
            })

        return JsonResponse({
            "status": "success",
            "items": favorites
        })


class ShopDetailView(APIView):
    """
    Возвращает поля Магазина и его Товары
    """

    filter_backends = (filters.OrderingFilter,)
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, *args, **kwargs):
        user = request.user
        db_type = db.connections.databases['default']['ENGINE']
        db_name = db_type.split(".")[-1]
        shop = get_object_or_404(Shop, slug=kwargs.get('slug'))
        q = request.GET.get("q")
        order = request.GET.get("order")
        category_slug = request.GET.get("category")
        products = shop.product_set.all()
        if q:
            if db_name == 'mysql' or db_name == 'postgresql':
                products = products.filter(Q(title__search=str(q)) |
                                           Q(short_description__search=str(q)))
            else:
                products = products.filter(Q(title__icontains=str(q)) |
                                           Q(short_description__icontains=str(q)))
        if order and order in ["price", "-price", "title", "created_at"]:
            products = products.order_by(order)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            if category.get_level() == 0:
                products = products.filter(category__id__in=[cat.id for cat in category.get_descendants()])
            else:
                products = products.filter(category=category)
        paginator = Paginator(products, 20)
        page = request.GET.get('page', 1)
        try:
            p = paginator.page(int(page))
        except (AttributeError, EmptyPage, ValueError):
            p = None
        products_dict = [model_to_dict(product) for product in p.object_list] if p else list()
        for prod in products_dict:
            product = get_object_or_404(Product, id=prod['id'])
            cart = user.cart_set.last() if user.is_authenticated() else None
            prod["is_in_cart"] = cart.cartitem_set.filter(product=product).exists() \
                if user.is_authenticated() and cart is not None else False
            prod["is_favorite"] = product.favorite.filter(user=user).exists() if user.is_authenticated() else False
            prod["main_image"] = product.get_main_thumb_image()
            prod["shop"] = shop.title
        shop_dict = model_to_dict(shop, exclude=['logo', 'user', 'logo_thumb'])
        shop_dict['logo'] = shop.logo_thumb.url if shop.logo_thumb else None
        shop_dict['users'] = [user.username for user in shop.user.all()]
        return JsonResponse({'status': 0,
                             'page': page if page else 1,
                             'shop': shop_dict if page is 1 else None,
                             'products': products_dict,
                             'count': paginator.count})

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super(ShopDetailView, self).dispatch(*args, **kwargs)


class Subscribe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsNotOwnerShop]

    def post(self, *args, **kwargs):
        shop_slug = self.request.POST.get("shop", "")
        shop = get_object_or_404(Shop, slug=shop_slug)
        user = self.request.user
        subcribe, create = Subscription.objects.get_or_create(user=user, subscription=shop)
        if not create:
            subcribe.delete()
            return JsonResponse({'status': 0, 'message': 'Вы успешно отписаны.'})
        return JsonResponse({'status': 0, 'message': 'Вы успешно подписаны.'})


class OrderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.filter(user=user, completed=False).first()

        cart.completed = True
        cart.save()

        serializer.save(cart=cart, user=user)
        send_letters_to_shop(cart)

        Cart.objects.create(user=user)

        return JsonResponse(dict(
            success=True, message='Order successfully created'
        ))


# class ShopSalesView(ListAPIView):
#     """
#     Возвращает поля Магазина и его Акции
#     """
#     serializer_class = SalesSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     pagination_class = ShopProductsLimitPagination
#     permission_classes = [AllowAny]
#     authentication_classes = (SessionAuthentication, TokenAuthentication)
#
#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         shop = Shop.objects.filter(slug=slug)
#         sales = Sales.objects.filter(shop=shop)
#         return sales


# class ShopReviewsView(ListAPIView):
#     """
#     Возвращает поля Магазина и его Отзывы
#     """
#     serializer_class = ShopReviewsSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     pagination_class = ShopProductsLimitPagination
#     permission_classes = [AllowAny]
#     authentication_classes = (SessionAuthentication, TokenAuthentication)
#
#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         shop = Shop.objects.filter(slug=slug)
#         reviews = ShopReviews.objects.filter(shop=shop)
#         return reviews


# class ShopContactsView(ListAPIView):
#     """
#     Возвращает поля Магазина и его Контакты
#     """
#     serializer_class = ShopContactsSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     pagination_class = ShopProductsLimitPagination
#     permission_classes = [AllowAny]
#     authentication_classes = (SessionAuthentication, TokenAuthentication)
#
#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         shop = Shop.objects.filter(slug=slug)
#         contacts = Contacts.objects.filter(shop=shop)
#         return contacts

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def search_products(request):
    db_type = db.connections.databases['default']['ENGINE']
    db_name = db_type.split(".")[-1]
    q = request.GET.get("q")
    if db_name == 'mysql' or db_name == 'postgresql':
        products = Product.objects.filter(Q(title__search=q) | Q(short_description__search=q))
    else:
        products = Product.objects.filter(Q(title__icontains=q) | Q(short_description__icontains=q))
    paginator = Paginator(products, 10)
    page = request.GET.get('page', 1)
    try:
        p = paginator.page(int(page))
    except (AttributeError, EmptyPage, ValueError):
        p = None
    product_list = list()
    if p:
        for product in p.object_list:
            product_list.append({
                "title": product.title,
                "slug": product.slug,
                "short_description": product.short_description,
                "shop": product.get_shop_title(),
                "main_image": product.get_main_thumb_image(),
                "price": product.get_price(),
                "is_favorite": product.favorite.filter(
                    user=request.user).exists() if request.user.is_authenticated else False,
                "is_in_cart": request.user.cart_set.last().cartitem_set.filter(product=product).exists() \
                    if request.user.is_authenticated \
                       and request.user.cart_set.all() \
                    else False
            })
    return JsonResponse({'status': 0,
                         'search_word': str(q),
                         'page': page if page else 1,
                         'result': product_list})

class ShopOrderList(APIView):
    permission_classes = [IsAuthenticated, IsOwnerShop4Shop]
    authentication_classes = [TokenAuthentication]

    def get(self, request, **kwargs):
        shop = get_object_or_404(Shop, slug=kwargs.get('slug'))
        orders = SimpleOrder.objects.filter(cart__cartitem__product__shop=shop, is_visible=True).distinct()
        orders_list = list()
        for order in orders:
            order_dict = model_to_dict(order, exclude=['confirm_shops', 'rejected_shops', 'status'])
            if shop in order.confirm_shops.all():
                order_dict['status'] = 'accepted'
            elif shop in order.rejected_shops.all():
                order_dict['status'] = 'rejected'
            else:
                order_dict['status'] = 'waiting'
            order_dict['total'] = order.cart.subtotal_for_shop(shop)
            order_dict['created_at'] = order.created_at
            orders_list.append(order_dict)
        return JsonResponse({'status': 0, 'orders': orders_list})


class CartDetailHistory(APIView):
    permission_classes = [IsAuthenticated, CartHistoryPerm]
    authentication_classes = [TokenAuthentication]

    def get(self, request, **kwargs):
        cart = get_object_or_404(Cart, id=kwargs.get('pk'))
        if cart.simpleorder.is_visible is True:
            items = list()
            for item in cart.cartitem_set.filter(product__shop__user=request.user):
                item_dict = model_to_dict(item)
                item_dict['image'] = item.product.get_main_thumb_image()
                item_dict['available'] = item.product.availability
                item_dict['title'] = item.product.title
                items.append(item_dict)
            return JsonResponse({'status': 0, 'items': items})
        return JsonResponse({'status': 1, 'message': 'This cart is in use'})

    def post(self, request, **kwargs):
        action = request.POST.get('action')
        shop = get_object_or_404(Shop, slug=request.POST.get('shop'))
        cart = get_object_or_404(Cart, id=kwargs.get('pk'))
        order = cart.simpleorder
        if action:
            if action == 'confirm':
                order.rejected_shops.remove(shop)
                order.confirm_shops.add(shop)
                order.save()
                return JsonResponse({'status': 0, 'message': 'Заказ успешно подтвержден.'})
            else:
                order.confirm_shops.remove(shop)
                order.rejected_shops.add(shop)
                order.save()
                return JsonResponse({'status': 0, 'message': 'Заказ отклонен.'})
        return JsonResponse({'status': 1, 'message': 'Action field is missing.'})
