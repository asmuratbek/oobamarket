# coding=utf-8
from __future__ import unicode_literals
from apps.category.models import Category
from django.db import models

# Create your models here.


class Filters(models.Model):
    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    title = models.CharField( max_length=255, unique=False, null=False, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, verbose_name='Категория')
    value = models.CharField(max_length=255, unique=False, null=True, verbose_name='Значение')

    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Обновлено')

    def __str__(self):
        return '{} - {}'.format(self.title, self.value)
