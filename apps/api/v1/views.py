import uuid
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_multiple_model.views import MultipleModelAPIView
from rest_auth.registration.views import SocialLoginView
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
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
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated)
from rest_framework.views import APIView
from slugify import slugify
from django.forms.models import model_to_dict
from apps.api.v1.serializers import *
from apps.cart.models import Cart, CartItem
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product, ProductImage, FavoriteProduct
from apps.shop.models import Shop, Contacts, Place
from apps.users.models import User, Subscription
from .pagination import (
    CategoryLimitPagination,
    ProductLimitPagination,
    ShopLimitPagination,
    ShopProductsLimitPagination
)
from .permissions import *

ORDER_TYPES = ["price", "-price", "title", "created_at"]


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    # pagination_class = ShopLimitPagination#PageNumberPagination
    queryset = Category.objects.all()


class ProductAddToFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

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
        from django.core.paginator import Paginator
        user = self.request.user
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
        p = Paginator(sorted_list, 10)
        pages_count = p.num_pages
        page = self.request.GET.get('page')
        if page and int(page) <= pages_count:
            p = p.page(int(page))
        else:
            p = p.page(1)
        items = list()
        for product in p.object_list:
            items.append({
                "title": product.title,
                "slug": product.slug,
                "short_description": product.short_description,
                "shop": product.get_shop_title(),
                "main_image": product.get_main_thumb_image(),
                "price": product.get_price(),
                "is_favorite": product.favorite.filter(
                    user=self.request.user).exists() if self.request.user.is_authenticated else False,
                "is_in_cart": self.request.user.cart_set.last().cartitem_set.filter(product=product).exists()\
                    if self.request.user.is_authenticated \
                       and self.request.user.cart_set.all() \
                    else False
            })
        return JsonResponse({
            "status": "success",
            "page": page if page else 1,
            "items" : items
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
        category = Category.objects.get(slug=slug)
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
                    Q(category__in=category.get_descendants()),
                ).order_by(order)
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


class GlobalCategoryDetailApiView(APIView):
    permission_classes = (AllowAny, )
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

        product_list = list()
        for product in products:
            product_list.append({
                "title": product.title,
                "slug": product.slug,
                "short_description": product.short_description,
                "shop": product.get_shop_title(),
                "main_image": product.get_main_thumb_image(),
                "price": product.get_price(),
                "is_favorite": product.favorite.filter(
                    user=self.request.user).exists() if self.request.user.is_authenticated else False,
                "is_in_cart": self.request.user.cart_set.last().cartitem_set.filter(product=product).exists()\
                    if self.request.user.is_authenticated \
                       and self.request.user.cart_set.all() \
                    else False
            })

        return JsonResponse({
            "status": "success",
            "products": product_list
        })


class MyListView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        cart_items = request.user.cart_set.last().cartitem_set.all().values("product__id") if request.user.cart_set.all() else False
        items = list()
        if cart_items:
            for item in cart_items:
                items.append({
                    "id": item.get("product__id")
                })
        favorites = request.user.favoriteproduct_set.all() if request.user.favoriteproduct_set.all() else False
        favs = list()
        if favorites:
            for fav in favorites:
                favs.append({
                    "id": fav.product.id
                })
        return JsonResponse({
            "favorites": favs if favs else [],
            "cart_items": items if items else []
        })


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
    authentication_classes = (TokenAuthentication,)

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
    serializer_class = ProductPostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerShop4Product]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

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
        product_dict['category'] = dict(id=product.category.id, title=product.category.title, slug=product.category.slug)
        return JsonResponse(dict(images=product_images, product=product_dict))

    def perform_update(self, serializer):
        remove_images_list = [int(i) for i in self.request.data.getlist('delete_images', [])
                                  if i != '' and i != None]
        delete_images = ProductImage.objects.filter(id__in=remove_images_list).delete()
        product = serializer.save(category=get_object_or_404(Category, slug=self.request.data.get('category', '')),
                                    shop=get_object_or_404(Shop, slug=self.request.data.get('shop', '')))
        images_files = self.request.FILES.getlist('images_files', '')
        if images_files:
            image_list = [ProductImage(product=product, image=img) for img in images_files]
            ProductImage.objects.bulk_create(image_list)
        return JsonResponse({'status': 0, 'message': 'Product is successfully updated.'})


class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


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
            "short_description": shop.short_description,
            "description": shop.description,
            "logo": shop.get_logo(),
            "is_owner": shop.is_owner(request.user) if is_authenticated else False,
            "is_subscribed": request.user.subscription_set.filter(subscription=shop).exists() if is_authenticated else False,
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
                "image": sale.image.url if sale.image else None
            })

        return JsonResponse({
            "status": "success",
            "sales": sales
        })

    def post(self, *args, **kwargs):
        self.permission_classes = [IsOwnerShop4Shop]
        shop = get_object_or_404(Shop, slug=kwargs.get('slug', ''))
        serializer = SalesSerializer(data=self.request.POST)
        if serializer.is_valid():
            serializer.save(shop=shop)
            return JsonResponse({'status': 0, 'message': 'Sale is successfully created.'})
        return JsonResponse({'status': 1, 'message': 'Sale values is not valid.'})


class ShopContactsView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        contact = shop.contacts_set.first()
        contact_dict = model_to_dict(contact, exclude=['place', 'latitude', 'longitude', 'shop'])
        if contact:
            contact_dict['latitude'] = contact.place.latitude if contact.place else contact.latitude
            contact_dict['longitude'] = contact.place.longitude if contact.place else contact.longitude
            contact_dict['place'] = contact.place.__str__() if contact.place else None
        return JsonResponse({
            "status": "success",
            "contacts": contact_dict
        })


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
                "stars": review.stars
            })

        return JsonResponse({
            "status": "success",
            "reviews": reviews
        })


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


class ShopUpdateApiView(RetrieveUpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwnerShop4Shop]
    authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=kwargs['slug'])
        shop_dict = model_to_dict(shop, exclude=['logo', 'user'])
        shop_dict['logo'] = shop.logo.url
        shop_dict['users'] = [user.id for user in shop.user.all()]
        shop_dict['contact'] = model_to_dict(shop.contacts_set.first())
        return JsonResponse(shop_dict)

    def perform_update(self, serializer):
        shop = serializer.save(user=[self.request.user.id])
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
                      if k != "shop" and contact_dict[k] != None and contact_dict[k] != ""]
        if contact:
            contact(**contact_dict)
            contact.save()
        else:
            if are_values:
                Contacts.objects.create(**contact_dict)



class ShopDeleteApiView(DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class ShopCreateApiView(CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        shop = serializer.save(user=[self.request.user.id],
                               slug=str(slugify(self.request.POST.get("title"))) + "-" + str(uuid.uuid4())[:4])
        place_id = self.request.POST.get("place_id")
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
            place=Place.objects.filter(id=place_id).first())
        are_values = [contact_dict[k] for k in contact_dict.keys()
                      if k != "shop" and contact_dict[k] != None and contact_dict[k] != ""]
        if are_values:
            contact = ShopContactsSerializer(data=contact_dict)
            if contact.is_valid():
                contact.save()


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
                "logo": shop.get_logo(),
                "short_description": shop.short_description,
                "email": shop.email
            })

        return JsonResponse({
            "status": "success",
            "shops": shops,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,
            "cart_count": user.get_cart_count(),
            "favorites_count": user.get_favorites_count()
        })


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
        for shop in user.cart_set.last().get_shops():
            items = list()
            for item in cartitems:
                if item.get('shop') == shop.title:
                    items.append(item)
            shops.append({
                "title": shop.title,
                "logo": shop.get_logo(),
                "items": items,
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
                "is_in_cart": self.request.user.cart_set.last().cartitem_set.filter(product=item.product).exists()\
                    if self.request.user.is_authenticated \
                       and self.request.user.cart_set.all() \
                    else False
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
