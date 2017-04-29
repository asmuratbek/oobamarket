from django.db import models

# Create your models here.
from django.urls import reverse


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
        return reverse("global_category:detail", kwargs={'slug': self.slug})

    def get_icon(self):
        return self.icon.url if self.icon else None
