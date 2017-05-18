from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from slugify import slugify

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

    def get_shop(self, obj):
        return str(obj.shop)


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
