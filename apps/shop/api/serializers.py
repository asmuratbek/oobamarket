from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from slugify import slugify

from apps.product.models import Shop


class ShopSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='shop_api:detail',
        lookup_field='slug'
    )

    update_url = HyperlinkedIdentityField(
        view_name='shop_api:update',
        lookup_field="slug"
    )

    delete_url = HyperlinkedIdentityField(
        view_name='shop_api:delete',
        lookup_field="slug"
    )

    used_categories = SerializerMethodField()

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
            'description',
            'short_description',
            'created_at',
            'updated_at',
            'logo',
            'get_absolute_url',
            'used_categories',

        )

    def get_used_categories(self, obj):
        return obj.get_used_categories()


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
