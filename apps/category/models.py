# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(MPTTModel):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    parent = TreeForeignKey('self', verbose_name='Родительская категория', max_length=10, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.CharField(max_length=32,verbose_name='Название на транслите', unique=True, blank=True, null=True)
    section = models.ForeignKey('GlobalCategory', verbose_name='Раздел', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Обновлено")

    def __str__(self):
        return self.title


class GlobalCategory(models.Model):

    class Meta:
        verbose_name = 'Глобальная категория'
        verbose_name_plural = 'Глобальные категории'

    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.CharField(max_length=32, verbose_name='Название на транслите')
    icon = models.ImageField(upload_to="category/icons", default=None)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Обновлено")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categories:global_detail", kwargs={'slug': self.slug})

    def get_icon(self):
        return self.icon.url if self.icon else None
