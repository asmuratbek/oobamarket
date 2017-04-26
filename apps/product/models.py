# coding=utf-8
from __future__ import unicode_literals
from apps.shop.models import Shop
from apps.category.models import Category
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class BestWeekProductsManager(models.Manager):

    def get_query_set(self):
        return super(BestWeekProductsManager, self).get_query_set()

class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    shop = models.ForeignKey(Shop, verbose_name='Название магазина')
    category = models.ForeignKey(Category, verbose_name='Название категории')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    price = models.DecimalField(null=True, blank=True, verbose_name='Цена', decimal_places=2, max_digits=10)
    sell_count = models.PositiveIntegerField(_("Количество продаж"), default=0)
    discount = models.DecimalField(null=True, blank=True, verbose_name='Скидка', decimal_places=2, max_digits=10)
    currency = models.CharField(null=True, max_length=255, verbose_name='Валюта')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    delivery_type = models.CharField(verbose_name='Вид доставки', max_length=255, null=True)
    delivery_cost = models.FloatField(verbose_name='Стоимость доставки', null=True)
    delivery_currency = models.CharField(null=True, max_length=255, verbose_name='Валюта доставки')
    # settings = models.ManyToManyField('ProductSettings', verbose_name='Характеристика')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии?')
    week_best = BestWeekProductsManager()

    def __str__(self):
        return "{shop} - {category} - {title}".format(shop=self.shop.title, category=self.category, title=self.title)

    def get_main_image(self):
        return self.productimage_set.first.image.url

    def get_shop_title(self):
        return self.shop.title

    def get_price(self):
        if self.discount:
            return '<span class="old-price"><strike>{}</strike></span>'.format((self.price * self.discount) / 100)
        else:
            return '<span>{}</span>'.format(self.price)


class ProductImage(models.Model):

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"

    product = models.ForeignKey(Product, verbose_name="Товар")
    image = models.ImageField(upload_to="products/image")
