# coding=utf-8
from __future__ import unicode_literals

import os
from io import BytesIO

from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models.signals import post_delete
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.conf import settings
from apps.category.models import Category
from apps.product.helpers import create_thumbnail_image
from apps.shop.models import Shop
from apps.users.models import User
from apps.utils.models import PublishBaseModel, Counter

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
CURRENCY_TYPES = (
    ('som', u'Сом'),
    ('dollar', u'$')
)


class ProductPublishedManager(models.Manager):
    def get_query_set(self):
        return super(ProductPublishedManager, self).get_query_set().filter(published=True)


class Product(PublishBaseModel, Counter):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-created_at',)

    shop = models.ForeignKey(Shop, verbose_name='Название магазина')
    category = models.ForeignKey(Category, verbose_name='Название категории')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(_("Название на транслите"), max_length=255, unique=True, blank=True, null=True)
    price = models.DecimalField(null=True, blank=True, verbose_name='Цена', decimal_places=0, max_digits=10)
    partner_price = models.DecimalField(null=True, blank=True, verbose_name='Цена для партнера', decimal_places=0, max_digits=10)
    sell_count = models.PositiveIntegerField(_("Количество продаж"), default=0, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='Скидка')
    currency = models.CharField(null=True, max_length=255, choices=CURRENCY_TYPES, verbose_name='Валюта', default='som')
    # quantity = models.IntegerField(verbose_name='Количество', default=0)
    delivery_type = models.CharField(verbose_name='Вид доставки', choices=DELIVERY_TYPES, blank=True, null=True,
                                     max_length=255)
    delivery_cost = models.FloatField(verbose_name='Стоимость доставки', default=0, null=True, blank=True)
    # settings = models.ManyToManyField('ProductSettings', verbose_name='Характеристика')
    availability = models.CharField(_("Наличие"), max_length=100, choices=AVAILABILITY_TYPES, default='available',
                                    blank=True, null=True)
    short_description = models.TextField(max_length=300, null=True, blank=True,
                                         verbose_name='Короткое описание товара до 300 символов')
    long_description = RichTextUploadingField(null=True, blank=True, verbose_name='Полное описание')
    # images = models.ManyToManyField('Media', verbose_name='Изображения продукта', blank=True)
    objects = ProductPublishedManager()
    meta_title = models.CharField(max_length=60, verbose_name='Мета заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=255, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, verbose_name='Мета ключевые слова', blank=True, null=True)
    seo_text = models.TextField(verbose_name='SEO Текст', null=True, blank=True)


    def __str__(self):
        return "{shop} - {category} - {title}".format(shop=self.shop.title, category=self.category, title=self.title)

    def get_main_image(self):
        if self.productimage_set.all():
            return self.productimage_set.first().image.url
        else:
            return settings.DEFAULT_IMAGE

    def get_main_thumb_image(self):
        if self.productimage_set.all():
            return self.productimage_set.first().thumb_image.url \
                    if self.productimage_set.first().thumb_image \
                    else self.productimage_set.first().image.url
        else:
            return settings.DEFAULT_IMAGE

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
        return "%s?item=%s&delete=True" % (reverse("cart:detail"), self.id)

    def get_update_url(self):
        return reverse("product:update_product", kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse("product:delete_product", kwargs={'slug': self.slug})

    def get_shop_url(self):
        return self.shop.get_absolute_url()

    def get_shop_slug(self):
        return self.shop.slug

    def get_category_title(self):
        return self.category.title

    def get_category_id(self):
        return self.category.id

    def get_category_slug(self):
        return self.category.slug

    def get_category_level(self):
        return self.category.get_level()

    def get_global_slug(self):
        return self.category.section.slug

    def get_parent_category_slug(self):
        if self.category.parent:
            return self.category.parent.slug
        else:
            return self.category.slug

    def get_parent_category_id(self):
        if self.category.parent:
            return self.category.parent.id
        else:
            return None

    def get_avatar_image(self):
        if self.productimage_set.filter(is_avatar=True):
            return self.productimage_set.filter(is_avatar=True).first().image.url
        else:
            return self.get_main_image()

    def get_avatar_thumb_image(self):
        if self.productimage_set.filter(is_avatar=True) and self.productimage_set.filter(is_avatar=True).first().thumb_image:
            return self.productimage_set.filter(is_avatar=True).first().thumb_image.url
        else:
            return self.get_main_thumb_image()


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
    image = models.ImageField(upload_to="products/image", max_length=300)
    thumb_image = models.ImageField(upload_to="products/thumb", max_length=300, null=True)
    is_avatar = models.BooleanField(verbose_name='Аватар продукта', default=False)

    def create_thumbnail(self):
        create_thumbnail_image(main_image=self.image, thumb_image=self.thumb_image, thumbnail_size=(480, 480))

    def save(self, *args, **kwargs):
        if self.image and self.is_avatar and not self.thumb_image:
            self.create_thumbnail()
        force_update = False
        if self.id:
            force_update = True
        super(ProductImage, self).save(force_update=force_update)


# def delete_files(sender, **kwargs):
#     image = kwargs.get('instance')
#     default_storage.delete(image.image.path)
#     if image.thumb_image:
#         default_storage.delete(image.thumb_image.path)
#
# post_delete.connect(delete_files, ProductImage)


currencies = [(t, c) for t, c in CURRENCY_TYPES if t != 'som']


class Currency(models.Model):
    currency_type = models.CharField(max_length=20, verbose_name='Тип валюты', choices=currencies)
    exchange_rate = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Курс')

    class Meta:
        verbose_name_plural = 'Курс валют'

    def __str__(self):
        return self.currency_type
