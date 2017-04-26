# coding=utf-8
from __future__ import unicode_literals
from ooba.shop.models import Shop
from ooba.category.models import Category
from django.db import models

# Create your models here.


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    shop = models.ForeignKey(Shop, verbose_name='Название магазина')
    category = models.ForeignKey(Category, verbose_name='Название категории')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    discount = models.FloatField(null=True, blank=True, verbose_name='Скидка')
    currency = models.CharField(null=True, max_length=255, verbose_name='Валюта')
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    delivery_type = models.CharField(verbose_name='Вид доставки', max_length=255, null=True)
    delivery_cost = models.FloatField(verbose_name='Стоимость доставки', null=True)
    delivery_currency = models.CharField(null=True, max_length=255, verbose_name='Валюта доставки')
    # settings = models.ManyToManyField('ProductSettings', verbose_name='Характеристика')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии?')

    def __str__(self):
        return "{shop} - {category} - {title}".format(shop=self.shop.title, category=self.category, title=self.title)
