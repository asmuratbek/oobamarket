# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.fields import  TreeForeignKey
from apps.global_category.models import GlobalCategory

class Ordering(models.Model):
    class Meta:
        abstract = True

    order = models.PositiveIntegerField(verbose_name='Очередь')

class Category(MPTTModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-updated_at']

    parent = TreeForeignKey('self', verbose_name='Родительская категория', max_length=10, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.CharField(max_length=32,verbose_name='Название на транслите', unique=True, blank=True, null=True)
    section = models.ForeignKey(GlobalCategory, verbose_name='Раздел', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Обновлено")
    order = models.PositiveIntegerField(verbose_name='Очередь', default=0)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    class MPTTMeta:
        order_insertion_by = ['order']

    # It is required to rebuild tree after save, when using order for mptt-tree
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={'slug': self.slug, 'global_slug': self.section.slug})

    def is_parent(self):
        return self.get_descendants().exists()

    def get_products(self):
        return self.product_set.all()
