from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from slugify import slugify

from apps.product.models import Category


class CategorySerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(
        view_name='category_api:detail',
        lookup_field='slug'
    )

    class Meta:
        model = Category
        fields = (
            'detail_url',
            'id',
            'title',
            'descendants',
            'created_at',
            'updated_at',
            )
