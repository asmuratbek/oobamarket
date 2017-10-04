from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.validators import UniqueTogetherValidator
from slugify import slugify

from apps.global_category.models import GlobalCategory
from apps.product.models import Category, ProductImage
from apps.reviews.models import ShopReviews
from apps.shop.models import Sales, Contacts, Place
from apps.users.models import User


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'parent_id'
            )


class ParentCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            )


class GlobalCategorySerializer(ModelSerializer):

    class Meta:
        model = GlobalCategory
        fields = (
            'id',
            'title',
            'slug',
            'icon'
            )

from apps.cart.models import Cart
from apps.product.models import Product


class ProductSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='api:product_detail',
        lookup_field='slug'
    )

    update_url = HyperlinkedIdentityField(
        view_name='api:product_update',
        lookup_field="slug"
    )

    delete_url = HyperlinkedIdentityField(
        view_name='api:product_delete',
        lookup_field="slug"
    )
    shop = SerializerMethodField()
    category_title = SerializerMethodField()
    is_owner = SerializerMethodField()
    main_image = SerializerMethodField()
    is_in_cart = SerializerMethodField()
    is_favorite = SerializerMethodField()
    detail_view = SerializerMethodField()
    update_view = SerializerMethodField()
    delete_view = SerializerMethodField()
    get_price_function = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'detail_url',
            'update_url',
            'delete_url',
            'id',
            'title',
            'short_description',
            'slug',
            'category_title',
            'shop',
            'discount',
            'published',
            'is_owner',
            'main_image',
            'is_in_cart',
            'is_favorite',
            'detail_view',
            'update_view',
            'delete_view',
            'get_price_function',
            'created_at',
            'updated_at',
        )

    def get_shop(self, obj):
        return str(obj.shop)

    def get_category_title(self, obj):
        return obj.category.title

    def get_get_price_function(self, obj):
        return obj.get_price()

    def get_is_owner(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.shop.is_owner(user) or user.is_staff
        return False

    def get_main_image(self, obj):
        return obj.get_avatar_image()

    def get_is_in_cart(self, product):
        request = self.context.get("request")
        if request.session.get("cart_id"):
            cart_id = request.session.get("cart_id")
            cart, created = Cart.objects.get_or_create(id=cart_id)
            if cart.cartitem_set.filter(product=product).exists():
                return True
            else:
                return False
        elif hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                if user.cart_set:
                    cart = user.cart_set.last()
                    if cart.cartitem_set.filter(product=product).exists():
                        return True
                else:
                    return False
        else:
            return False

    def get_is_favorite(self, product):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                if product.favorite.filter(user=user).exists():
                    return True
                else:
                    return False

    def get_detail_view(self, obj):
        return obj.get_absolute_url()

    def get_update_view(self, obj):
        return obj.get_update_url()

    def get_delete_view(self, obj):
        return obj.get_delete_url()


class ProductDetailSerializer(ModelSerializer):
    update_url = HyperlinkedIdentityField(
        view_name='api:product_update',
        lookup_field="slug"
    )

    delete_url = HyperlinkedIdentityField(
        view_name='api:product_delete',
        lookup_field="slug"
    )
    shop = SerializerMethodField()
    price = SerializerMethodField()
    category_title = SerializerMethodField()
    is_owner = SerializerMethodField()
    main_image = SerializerMethodField()
    is_in_cart = SerializerMethodField()
    is_favorite = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'update_url',
            'delete_url',
            'id',
            'title',
            'short_description',
            "long_description",
            'slug',
            'category_title',
            'shop',
            'currency',
            'published',
            'is_owner',
            'main_image',
            'is_in_cart',
            'is_favorite',
            'price',
            'created_at',
            'updated_at',
            'get_category_title'
        )

    def get_shop(self, obj):
        return str(obj.shop)

    def get_price(self, obj):
        return obj.get_price()

    def get_category_title(self, obj):
        return obj.category.title

    def get_is_owner(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.shop.is_owner(user) or user.is_staff
        return False

    def get_main_image(self, obj):
        return obj.get_avatar_image()

    def get_is_in_cart(self, product):
        request = self.context.get("request")
        if request.session.get("cart_id"):
            cart_id = request.session.get("cart_id")
            cart, created = Cart.objects.get_or_create(id=cart_id)
            if cart.cartitem_set.filter(product=product).exists():
                return True
            else:
               return False
        else:
            return False

    def get_is_favorite(self, product):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                if product.favorite.filter(user=user).exists():
                    return True
                else:
                    return False


class ProductCreateSerializer(ModelSerializer):

    class Meta:
        model = Product
        exclude = ('id', 'slug', 'created_at', 'updated_at', 'counter', 'currency',
                   'partner_price', 'sell_count', 'delivery_type', 'delivery_cost',
                   'availability', 'meta_title', 'meta_description', 'meta_keywords', 'seo_text',
                   'long_description',)

    shop = serializers.CharField(max_length=300)
    category = serializers.CharField(max_length=300)

    # def get_slug(self, obj):
    #     return slugify(obj.title)


class ProductImageSerializer(ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            'image',
        )


from apps.product.models import Shop


class ShopSerializer(ModelSerializer):
    # detail_url = HyperlinkedIdentityField(
    #     view_name='api:shop_detail',
    #     lookup_field='slug'
    # )
    #
    # update_url = HyperlinkedIdentityField(
    #     view_name='api:shop_update',
    #     lookup_field="slug"
    # )
    #
    # delete_url = HyperlinkedIdentityField(
    #     view_name='api:shop_delete',
    #     lookup_field="slug"
    # )

    # used_categories = SerializerMethodField()
    is_owner = SerializerMethodField()
    phone = SerializerMethodField()
    is_authenticated = SerializerMethodField()
    is_subscribed = SerializerMethodField()
    places = SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            # 'detail_url',
            # 'update_url',
            # 'delete_url',
            'id',
            'title',
            'slug',
            'user',
            'email',
            'phone',
            'places',
            'is_authenticated',
            'is_subscribed',
            'is_owner',
            'description',
            'short_description',
            'created_at',
            'updated_at',
            'logo',
            'get_absolute_url',
            # 'used_categories',

        )


    # def get_used_categories(self, obj):
    #     return obj.get_used_categories()

    def get_is_owner(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.is_owner(user)
        return False

    def get_phone(self, obj):
        if obj.contacts_set.first():
            return obj.contacts_set.first().phone
        else:
            return None

    def get_is_authenticated(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                return True
            else:
                return False

    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                subs = [sub.subscription.id for sub in user.subscription_set.all()]
                if obj.id in subs:
                    return True
                else:
                    return False
            else:
                return False

    def get_places(self, obj):
        places = [contact.place.id if contact.place else None for contact in obj.contacts_set.all()]
        return places


class ShopCreateSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = Shop
        validators = [
            UniqueTogetherValidator(
                queryset=Shop.objects.all(),
                fields=('slug',)
            )
        ]
        fields = (
            'id',
            'title',
            'slug',
            'user',
            'email',
            'description',
            'short_description',
            'created_at',
            'updated_at',
            'logo'
        )


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'address'
        )


class SalesSerializer(ModelSerializer):

    class Meta:
        model = Sales
        fields = (
            'id',
            'title',
            'short_description',
            'description',
            'discount',
            'image',
            'created_at',
            'updated_at'
        )


class ShopReviewsSerializer(ModelSerializer):

    username = SerializerMethodField()

    class Meta:
        model = ShopReviews
        fields = (
            'id',
            'username',
            'text',
            'stars',
            'created_at',
            'updated_at'
        )

    def get_username(self, obj):
        return obj.user.username if obj.user.username else obj.user.email


class ShopContactsSerializer(ModelSerializer):
    """
       API endpoint that allows users to be viewed or edited.

       retrieve:
       Return a user instance.

       list:
       Return all users, ordered by most recently joined.
       """

    class Meta:
        model = Contacts
        fields = (
            'id',
            'address',
            'phone',
            'place',
            'latitude',
            'longitude',
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
            'round_the_clock',
            'created_at',
            'updated_at'

        )


class PlaceSerializer(ModelSerializer):

    class Meta:
        model = Place
        fields = (
            'id',
            'title',
            'ttype',
        )

    ttype = SerializerMethodField()


    def get_ttype(self, obj):
        return obj.get_type_display()
