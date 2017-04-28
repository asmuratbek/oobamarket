# coding=utf-8
from __future__ import unicode_literals
from django.urls import reverse
from apps.users.models import User
from django.db import models
# Create your models here.



class Shop(models.Model):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    user = models.ManyToManyField(to=User, verbose_name='Администратор магазина')
    title = models.CharField(max_length=255, verbose_name='Название магазина')
    slug = models.CharField(max_length=32, verbose_name='Название на транслите')
    email = models.EmailField(verbose_name='E-mail магазина')
    short_decription = models.TextField(max_length=300, verbose_name='Короткое описание магазина')
    description = models.TextField(max_length=1500, verbose_name='Полное описание магазина')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Создано')
    updated_ad = models.DateTimeField(auto_now_add=True, verbose_name='Обновленно')
    logo = models.ImageField(upload_to='images/shop/logo/', null=True,
                                verbose_name='Логотип')
    banner = models.ForeignKey('Banners', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shops:detail", kwargs={'slug': self.slug})

    def get_logo(self):
        return self.logo.url

    def get_shop_user(self):
        return str(self.user.username)

class Banners(models.Model):
    class Meta:
        verbose_name = 'Баннер магазина'
        verbose_name_plural = 'Баннеры магазинов'

    title = models.CharField(max_length=255, verbose_name='Название баннера', blank=True, null=True)
    image = models.ImageField(upload_to='images/shop/banners/', verbose_name='Изображение банера')

    def save(self, *args, **kwargs):
        super(Banners, self).save(*args, **kwargs)
        self.title = str(self.image)

    def __str__(self):
        return self.title
