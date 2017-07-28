from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from slugify import slugify

from apps.product.models import Category


class GlobalCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            )
