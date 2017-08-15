from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from slugify import slugify
from apps.product.models import Category
from apps.global_category.models import GlobalCategory


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'descendants',
            'created_at',
            'updated_at',
            )


class GlobalCategorySerializer(ModelSerializer):

    class Meta:
        model = GlobalCategory
        fields = (
            'id',
            'title',
            'slug',
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
    delivery_type_display = SerializerMethodField()
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
            'price',
            'sell_count',
            'discount',
            'currency',
            'delivery_type',
            'delivery_cost',
            'availability',
            'published',
            'is_owner',
            'main_image',
            'is_in_cart',
            'delivery_type_display',
            'is_favorite',
            'detail_view',
            'update_view',
            'delete_view',
            'get_price_function',
            'created_at',
            'updated_at',
            'get_category_title'
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

    def get_delivery_type_display(self, obj):
        return obj.get_delivery_type()

    def get_main_image(self, obj):
        return obj.get_main_image()

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

    def get_detail_view(self, obj):
        return obj.get_absolute_url()

    def get_update_view(self, obj):
        return obj.get_update_url()

    def get_delete_view(self, obj):
        return obj.get_delete_url()


class ProductCreateSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'category',
            'shop',
            'price',
            'discount',
            'currency',
            'published',
        )

    slug = SerializerMethodField()

    def get_slug(self, obj):
        return slugify(obj.title)


from apps.product.models import Shop


class ShopSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='api:shop_detail',
        lookup_field='slug'
    )

    update_url = HyperlinkedIdentityField(
        view_name='api:shop_update',
        lookup_field="slug"
    )

    delete_url = HyperlinkedIdentityField(
        view_name='api:shop_delete',
        lookup_field="slug"
    )

    # used_categories = SerializerMethodField()
    is_owner = SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            'detail_url',
            'update_url',
            'delete_url',
            'id',
            'title',
            'user',
            'email',
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
            return obj.is_owner(user) or user.is_staff
        return False


class ShopCreateSerializer(ModelSerializer):

    class Meta:
        model = Shop
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

    slug = SerializerMethodField()

    def get_slug(self, obj):
        return slugify(obj.title)
