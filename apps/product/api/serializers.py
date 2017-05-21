from django.utils.safestring import mark_safe
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from slugify import slugify

from apps.cart.models import Cart
from apps.product.models import Product


class ProductSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='product_api:detail',
        lookup_field='slug'
    )

    update_url = HyperlinkedIdentityField(
        view_name='product_api:update',
        lookup_field="slug"
    )

    delete_url = HyperlinkedIdentityField(
        view_name='product_api:delete',
        lookup_field="slug"
    )
    shop = SerializerMethodField()
    shop_title = SerializerMethodField()
    is_owner = SerializerMethodField()
    main_image = SerializerMethodField()
    is_in_cart = SerializerMethodField()
    delivery_type_display = SerializerMethodField()
    is_favorite = SerializerMethodField()
    detail_view = SerializerMethodField()
    update_view = SerializerMethodField()
    get_price_function = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'detail_url',
            'update_url',
            'delete_url',
            'id',
            'title',
            'category',
            'shop',
            'shop_title',
            'price',
            'sell_count',
            'discount',
            'currency',
            'quantity',
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
            'get_price_function'
        )

    def get_shop(self, obj):
        return str(obj.shop)

    def get_get_price_function(self, obj):
        return obj.get_price()

    def get_shop_title(self, obj):
        return str(obj.get_shop_title())

    def get_is_owner(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.shop.is_owner(user)
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


class ProductCreateSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'category',
            'shop',
            'price',
            'sell_count',
            'discount',
            'currency',
            'quantity',
            'delivery_type',
            'delivery_cost',
            'availability',
            'published',
        )

    slug = SerializerMethodField()

    def get_slug(self, obj):
        return slugify(obj.title)
