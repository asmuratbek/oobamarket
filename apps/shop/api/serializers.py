from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from apps.product.models import Shop

"""
    user = models.ManyToManyField(to=User, verbose_name='Администратор магазина')
    title = models.CharField(max_length=255, verbose_name='Название магазина')
    slug = models.CharField(max_length=32, verbose_name='Название на транслите', unique=True)
    phone = models.CharField(_("Телефон"), max_length=20, default='')
    email = models.EmailField(verbose_name='E-mail магазина')
    short_description = models.TextField(max_length=300, verbose_name='Короткое описание магазина')
    description = models.TextField(max_length=1500, verbose_name='Полное описание магазина')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Создано')
    updated_ad = models.DateTimeField(auto_now_add=True, verbose_name='Обновленно')
    logo = models.ImageField(upload_to='images/shop/logo/', null=True,
                             verbose_name='Логотип')

"""
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

    class Meta:
        model = Shop
        fields = (
            'detail_url',
            'update_url',
            'delete_url',
            'id',
            'title',
            'user',
            'phone',
            'email',
            'description',
            'short_description',
            'created_at',
            'updated_at',
            'logo'

        )


class ShopCreateSerializer(ModelSerializer):

    class Meta:
        model = Shop
        fields = (
            'id',
            'title',
            'user',
            'phone',
            'email',
            'description',
            'short_description',
            'created_at',
            'updated_at',
            'logo'
        )
