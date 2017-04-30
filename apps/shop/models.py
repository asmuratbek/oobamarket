# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

from apps.category.models import Category
from apps.users.models import User

# Create your models here.
SOCIAL_LINKS = (
    ('facebook', u'Facebook.com'),
    ('vk', u'Vk.com'),
    ('ok', u'Odnoklassniki.ru'),
    ('instagram', u'Instagram.com')
)


class Shop(models.Model):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    user = models.ManyToManyField(to=User, verbose_name='Администратор магазина')
    title = models.CharField(max_length=255, verbose_name='Название магазина')
    slug = models.CharField(max_length=32, verbose_name='Название на транслите')
    phone = models.CharField(_("Телефон"), max_length=20, default='')
    email = models.EmailField(verbose_name='E-mail магазина')
    short_description = models.TextField(max_length=300, verbose_name='Короткое описание магазина')
    description = models.TextField(max_length=1500, verbose_name='Полное описание магазина')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Создано')
    updated_ad = models.DateTimeField(auto_now_add=True, verbose_name='Обновленно')
    logo = models.ImageField(upload_to='images/shop/logo/', null=True,
                             verbose_name='Логотип')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shops:detail", kwargs={'slug': self.slug})

    def get_logo(self):
        return self.logo.url

    def get_shop_user(self):
        return str(self.user.username)

    def get_shop_products(self):
        return self.product_set.all()[:6]

    def get_used_categories(self):
        category_ids = list()
        for product in self.product_set.all():
            category_ids.append(product.category.id)
        categories = Category.objects.filter(id__in=category_ids)
        return categories

    def get_global_category(self):
        return self.product_set.first().category.section


class Banners(models.Model):
    class Meta:
        verbose_name = 'Баннер магазина'
        verbose_name_plural = 'Баннеры магазинов'

    title = models.CharField(max_length=255, verbose_name='Название баннера', blank=True, null=True)
    image = models.ImageField(upload_to='images/shop/banners/', verbose_name='Изображение банера')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Banners, self).save(*args, **kwargs)
        self.title = str(self.image)

    def __str__(self):
        return self.title


class SocialLinks(models.Model):
    class Meta:
        verbose_name = 'Социальная ссылка'
        verbose_name_plural = 'Социальные ссылки'

    link = models.CharField(max_length=255, verbose_name='Ссылка на страницу соц.сети')
    icon = models.CharField(max_length=255, choices=SOCIAL_LINKS, verbose_name='Выбор соц. иконки', default=None)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def get_icon(self):
        return self.get_icon_display()

    def __str__(self):
        return self.shop
