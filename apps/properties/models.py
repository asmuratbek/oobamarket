from django.db import models

# Create your models here.
from apps.category.models import Category, Ordering


class Properties(Ordering):
    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    category = models.ForeignKey(Category, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Название параметра')

    def __str__(self):
        return self.title

class Values(Ordering):
    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'

    properties = models.ForeignKey(Properties, verbose_name='Параметр')
    category = models.ForeignKey(Category, verbose_name='Категория')
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return self.value
