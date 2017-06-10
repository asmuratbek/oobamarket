# coding=utf-8
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

from apps.category.models import Category
from apps.shop.models import Shop
from apps.users.models import User
from apps.utils.models import PublishBaseModel

DELIVERY_TYPES = (
    ('self', u'Самовывоз'),
    ('paid', u'Платная доставка'),
    ('free', u'Бесплатная доставка')
)

AVAILABILITY_TYPES = (
    ('available', u'В наличии'),
    ('waiting', u'Ожидается'),
    ('not_available', u'Нет в наличии')
)


class ProductPublishedManager(models.Manager):
    def get_query_set(self):
        return super(ProductPublishedManager, self).get_query_set().filter(published=True)


class Product(PublishBaseModel):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-created_at',)

    shop = models.ForeignKey(Shop, verbose_name='Название магазина')
    category = models.ForeignKey(Category, verbose_name='Название категории')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(_("Название на транслите"), max_length=50, unique=True, blank=True, null=True)
    price = models.DecimalField(null=True, blank=True, verbose_name='Цена', decimal_places=0, max_digits=10)
    sell_count = models.PositiveIntegerField(_("Количество продаж"), default=0, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='Скидка')
    currency = models.CharField(null=True, max_length=255, verbose_name='Валюта', default='сом')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    delivery_type = models.CharField(verbose_name='Вид доставки', choices=DELIVERY_TYPES, default='self',
                                     max_length=255)
    delivery_cost = models.FloatField(verbose_name='Стоимость доставки', default=0, null=True, blank=True)
    # settings = models.ManyToManyField('ProductSettings', verbose_name='Характеристика')
    availability = models.CharField(_("Наличие"), max_length=100, choices=AVAILABILITY_TYPES, default='available')
    short_description = models.TextField(max_length=300, null=True, blank=True,
                                         verbose_name='Короткое описание товара до 300 символов')
    long_description = RichTextUploadingField(null=True, blank=True, verbose_name='Полное описание')
    # images = models.ManyToManyField('Media', verbose_name='Изображения продукта', blank=True)
    objects = ProductPublishedManager()
    values = models.ManyToManyField('properties.Values', verbose_name='Характеристики', blank=True)

    def __str__(self):
        return "{shop} - {category} - {title}".format(shop=self.shop.title, category=self.category, title=self.title)

    def get_main_image(self):
        if self.productimage_set.all():
            return self.productimage_set.first().image.url
        else:
            return None

    def get_all_images(self):
        return self.productimage_set.all()

    def get_shop_title(self):
        return self.shop.title

    def get_shop(self):
        return self.shop

    def get_price(self):
        if self.discount:
            return self.price - ((self.price * self.discount) / 100)
        else:
            return self.price

    def get_delivery_type(self):
        return self.get_delivery_type_display()

    def get_availability(self):
        return self.get_availability_display()

    def get_absolute_url(self):
        return reverse("categories:product_detail", kwargs={'slug': self.slug,
                                                            'category_slug': self.category.slug,
                                                            'global_slug': self.category.section.slug})

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart:detail"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" % (reverse("cart:detail"), self.id)

    def get_update_url(self):
        return reverse("product:update_product", kwargs={'slug': self.slug})

    def get_shop_url(self):
        return self.shop.get_absolute_url()


class FavoriteProduct(models.Model):
    class Meta:
        verbose_name_plural = "Избранные продукты"
        verbose_name = "Избранный продукт"

    product = models.ForeignKey(Product, related_name='favorite')
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

    def get_absolute_url(self):
        return self.product.get_absolute_url()


class ProductImage(models.Model):
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", null=True)
    image = models.ImageField(upload_to="products/image")

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ProductImage, self).delete(*args, **kwargs)
        storage.delete(path)
