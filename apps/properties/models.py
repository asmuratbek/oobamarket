from django.db import models

# Create your models here.
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from apps.category.models import Category, Ordering
from apps.product.models import Product


class Properties(MPTTModel, Ordering):
    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'

    category = models.ManyToManyField(Category, verbose_name='Категория', blank=True)
    title = models.CharField(max_length=255, verbose_name='Название параметра')
    slug = models.CharField(max_length=255, verbose_name='Slug', unique=True)
    parent = TreeForeignKey('self', verbose_name='Родительская категория', null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_property_from_category(self):
        return self.objects.filter(category__in__id=self.category.id)


class Values(Ordering):
    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'

    properties = models.ForeignKey(Properties, verbose_name='Параметр', blank=True)
    value = models.CharField(max_length=255, verbose_name='Значение')
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.value
