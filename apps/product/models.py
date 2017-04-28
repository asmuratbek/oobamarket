# coding=utf-8
from __future__ import unicode_literals
from apps.shop.models import Shop
from apps.category.models import Category
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
from apps.users.models import User

DELIVERY_TYPES = (
    ('self', u'Самовывоз'),
    ('paid', u'Платная доставка'),
    ('free', u'Бесплатная доставка')
)


class ProductPublishedManager(models.Manager):
    def get_query_set(self):
        return super(ProductPublishedManager, self).get_query_set().filter(published=True)


class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    shop = models.ForeignKey(Shop, verbose_name='Название магазина')
    category = models.ForeignKey(Category, verbose_name='Название категории')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(_("Название на транслите"), max_length=50, unique=True, blank=True, null=True)
    price = models.DecimalField(null=True, blank=True, verbose_name='Цена', decimal_places=0, max_digits=10)
    sell_count = models.PositiveIntegerField(_("Количество продаж"), default=0)
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='Скидка')
    currency = models.CharField(null=True, max_length=255, verbose_name='Валюта', default='сом')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    delivery_type = models.CharField(verbose_name='Вид доставки', choices=DELIVERY_TYPES, default='self', max_length=255)
    delivery_cost = models.FloatField(verbose_name='Стоимость доставки', null=True)
    delivery_currency = models.CharField(null=True, max_length=255, verbose_name='Валюта доставки')
    # settings = models.ManyToManyField('ProductSettings', verbose_name='Характеристика')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии?')
    published = models.BooleanField(default=True)
    objects = ProductPublishedManager()

    def __str__(self):
        return "{shop} - {category} - {title}".format(shop=self.shop.title, category=self.category, title=self.title)

    def get_main_image(self):
        if self.productimage_set.all():
            return self.productimage_set.first().image.url
        else:
            return None

    def get_shop_title(self):
        return self.shop.title

    def get_price(self):
        if self.discount:
            return (self.price * self.discount) / 100
        else:
            return self.price

    def get_delivery_type(self):
        return self.get_delivery_type_display()


class FavoriteProduct(models.Model):

    class Meta:
        verbose_name_plural = "Избранные продукты"
        verbose_name = "Избранный продукт"

    product = models.OneToOneField(Product, related_name='related_product')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.product.__str__()

    def get_main_image(self):
        return self.product.get_main_image()

    def get_shop_title(self):
        return self.product.get_shop_title()

    def get_price(self):
        return self.product.get_price()

    def get_delivery_type(self):
        return self.product.delivery_type

    def get_delivery_type_display(self):
        return self.product.get_delivery_type()

    def is_discount(self):
        return self.product.discount

    def get_currency(self):
        return self.product.currency

    def get_old_price(self):
        return self.product.price

    def get_title(self):
        return self.product.title


class ProductImage(models.Model):

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    product = models.ForeignKey(Product, verbose_name="Товар")
    image = models.ImageField(upload_to="products/image")
