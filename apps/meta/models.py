from django.db import models


# Create your models here.
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.shop.models import Shop


class MetaData(models.Model):
    class Meta:
        verbose_name = 'Метаданные'
        verbose_name_plural = 'Метаданные'

    h1 = models.CharField(max_length=225, verbose_name='Н1 заголовок', blank=True, null=True)
    title = models.CharField(max_length=70, verbose_name='Мета название', blank=True, null=True)
    description = models.TextField(max_length=140, verbose_name='Мета описание', blank=True, null=True)
    keywords = models.CharField(max_length=255, verbose_name='Ключевые слова', blank=True, null=True)
    seo_text = models.TextField(verbose_name='Сео текст', null=True, blank=True)
    url = models.CharField(max_length=255, verbose_name='УРЛ', blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    global_category = models.ForeignKey(GlobalCategory, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.title

    def get_h1(self):
        return str(self.title)

