# coding=utf-8
from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import ugettext as _

from apps.users.models import User
from apps.utils.models import PublishBaseModel

# Create your models here.
SOCIAL_LINKS = (
    ('facebook', u'Facebook.com'),
    ('vk', u'Vk.com'),
    ('ok', u'Odnoklassniki.ru'),
    ('instagram', u'Instagram.com')
)


class Shop(PublishBaseModel):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    user = models.ManyToManyField(to=User, verbose_name='Администратор магазина')
    title = models.CharField(max_length=255, verbose_name='Название магазина')
    slug = models.CharField(max_length=32, verbose_name='Название на транслите', unique=True)
    phone = models.CharField(_("Телефон"), max_length=20, default='')
    email = models.EmailField(verbose_name='E-mail магазина')
    short_description = models.TextField(verbose_name='Короткое описание магазина')
    description = models.TextField(verbose_name='Полное описание магазина')
    logo = models.ImageField(upload_to='images/shop/logo/', null=True,
                             verbose_name='Логотип', blank=True)

    def __str__(self):
        return self.title

    def get_shop_name(self):
        return str(self.user.shop.title)

    def get_absolute_url(self):
        return reverse("shops:detail", kwargs={'slug': self.slug})

    def get_logo(self):
        return self.logo.url

    def get_shop_user(self):
        return str(self.user.username)

    def get_shop_products(self):
        return self.product_set.all()[:6]

    def get_products_count(self):
        return self.product_set.count()

    def create_shop(self):
        return reverse('shops:create')

    def get_used_categories(self):
        from apps.category.models import Category
        category_ids = list()
        for product in self.product_set.all():
            category_ids.append(product.category.id)
        categories = Category.objects.filter(id__in=category_ids)
        return categories

    def get_global_category(self):
        if self.product_set.exists():
            return self.product_set.first().category.section

    def get_update_url(self):
        return reverse('shops:update', kwargs={'slug': self.slug})

    def send_email(self, subject, message):
        send_mail(subject, message, 'asmnotifications@gmail.com', [self.email, ])

    def is_owner(self, user):
        return True if len(self.user.filter(id=user.id)) > 0 else False




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

    facebook = models.CharField(max_length=255, verbose_name='Facebook', null=True, blank=True)
    vk = models.CharField(max_length=255, verbose_name='VK', null=True, blank=True)
    instagram = models.CharField(max_length=255, verbose_name='Instagram', null=True, blank=True)
    twitter =  models.CharField(max_length=255, verbose_name='Twitter', null=True, blank=True)
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.shop)


def create_social_links(sender, **kwargs):
    if kwargs['created']:
        social_links = SocialLinks.objects.create(shop=kwargs['instance'])

post_save.connect(create_social_links, sender=Shop)
