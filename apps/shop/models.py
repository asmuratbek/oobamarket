# coding=utf-8
from __future__ import unicode_literals
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import ugettext as _
from slugify import slugify
from apps.product.helpers import create_thumbnail_image

from config.settings import base as settings
from apps.users.models import User
from apps.utils.models import PublishBaseModel, Counter, MetaBaseModel, PostionMapModel


# Create your models here.
SOCIAL_LINKS = (
    ('facebook', u'Facebook.com'),
    ('vk', u'Vk.com'),
    ('ok', u'Odnoklassniki.ru'),
    ('instagram', u'Instagram.com')
)

DAYS = (
    ('monday', "Понедельник"),
    ('tuesday', "Вторник"),
    ('wednesday', "Среда"),
    ('thursday', "Четверг"),
    ('friday', "Пятница"),
    ('saturday', "Суббота"),
    ('sunday', "Воскресенье"),
)


class Shop(PublishBaseModel, MetaBaseModel, Counter):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    user = models.ManyToManyField(to=User, verbose_name='Администратор магазина')
    title = models.CharField(max_length=30, verbose_name='Название магазина')
    slug = models.CharField(max_length=32, verbose_name='Название на транслите', unique=True)
    email = models.EmailField(verbose_name='E-mail магазина')
    short_description = models.TextField(verbose_name='Короткое описание магазина', null=True, blank=True)
    description = models.TextField(verbose_name='Полное описание магазина', blank=True, null=True)
    logo = models.ImageField(upload_to='images/shop/logo/', null=True, blank=True,
                             verbose_name='Логотип')
    logo_thumb = models.ImageField(upload_to='images/shop/thumb/', null=True, blank=True)

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_img = self.logo

    def save(self, *args, **kwargs):
        if (self.logo and not self.pk) or (self.logo and self.logo != self.current_img):
            self.create_thumbnail()
        if not self.slug:
            self.slug = slugify(self.title)
        super(Shop, self).save(*args, **kwargs)

    def get_slug(self):
        return self.slug

    def get_shop_name(self):
        return str(self.user.shop.title)

    def get_absolute_url(self):
        return reverse("shops:detail", kwargs={'slug': self.slug})

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return settings.DEFAULT_IMAGE

    def get_logo_thumb(self):
        if self.logo_thumb:
            return self.logo_thumb.url
        return settings.DEFAULT_IMAGE

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
        category_ids = self.product_set.values_list('category_id')
        categories = Category.objects.filter(id__in=category_ids)
        return categories

    def get_parent_categories_of_used(self):
        from apps.category.models import Category
        categories = self.get_used_categories()
        parent_categories_ids = []

        for i in categories:
            if i.parent:
                parent_categories_ids.append(i.parent.id)

        parents = Category.objects.filter(id__in=parent_categories_ids).distinct() if len(
            parent_categories_ids) > 0 else Category.objects.none()

        return parents

    def get_used_categories_title(self):
        return ", ".join([i.title for i in self.get_used_categories()])

    def get_used_category_ids(self):
        return [i.id for i in self.get_used_categories()]

    def get_global_category(self):
        if self.product_set.exists():
            return self.product_set.first().category.section

    def get_update_url(self):
        return reverse('shops:update', kwargs={'slug': self.slug})

    def send_email(self, subject, message):
        send_mail(subject, message, 'asmnotifications@gmail.com', [self.email, ])

    def is_owner(self, user):
        return True if len(self.user.filter(id=user.id)) > 0 else False

    def create_thumbnail(self):
        create_thumbnail_image(main_image=self.logo, thumb_image=self.logo_thumb, thumbnail_size=(480, 480))


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
        return self.shop.title


class Contacts(PublishBaseModel, PostionMapModel):
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    address = models.CharField(verbose_name='Адрес', max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', null=True, blank=True)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', null=True)
    place = models.ForeignKey('Place', verbose_name='Торговая точка', null=True, blank=True)
    monday = models.CharField(max_length=255, verbose_name='Понедельник', null=True, blank=True)
    tuesday = models.CharField(max_length=255, verbose_name='Вторник', null=True, blank=True)
    wednesday = models.CharField(max_length=255, verbose_name='Среда', null=True, blank=True)
    thursday = models.CharField(max_length=255, verbose_name='Четверг', null=True, blank=True)
    friday = models.CharField(max_length=255, verbose_name='Пятница', null=True, blank=True)
    saturday = models.CharField(max_length=255, verbose_name='Суббота', null=True, blank=True)
    sunday = models.CharField(max_length=255, verbose_name='Воскресенье', null=True, blank=True)
    round_the_clock = models.BooleanField(default=False, verbose_name='Круглосуточно')

    def __str__(self):
        return "{} - {}".format(self.address, self.shop)


class SocialLinks(models.Model):
    class Meta:
        verbose_name = 'Социальная ссылка'
        verbose_name_plural = 'Социальные ссылки'

    facebook = models.CharField(max_length=255, verbose_name='Facebook', null=True, blank=True)
    vk = models.CharField(max_length=255, verbose_name='VK', null=True, blank=True)
    instagram = models.CharField(max_length=255, verbose_name='Instagram', null=True, blank=True)
    twitter = models.CharField(max_length=255, verbose_name='Twitter', null=True, blank=True)
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.shop)


def create_social_links(sender, **kwargs):
    if kwargs['created']:
        social_links = SocialLinks.objects.create(shop=kwargs['instance'])


post_save.connect(create_social_links, sender=Shop)

PlACE_TYPE = (
    ('mall', "ТЦ"),
    ('market', "Рынок")
)


class Place(PublishBaseModel, PostionMapModel):
    class Meta:
        verbose_name = "Торговая точка"
        verbose_name_plural = "Торговые точки"
        ordering = ('title',)

    title = models.CharField(_("Название"), max_length=255)
    type = models.CharField(_("Тип торговой точки"), choices=PlACE_TYPE, max_length=255)

    def __str__(self):
        return "{}-{}".format(self.get_type_display(), self.title)


class Sales(PublishBaseModel):
    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['-created_at']

    shop = models.ForeignKey(Shop, verbose_name='Магазин', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name='Название акции')
    short_description = models.TextField(max_length=155, verbose_name='Короткое описание')
    description = RichTextUploadingField(null=True, blank=True)
    discount = models.IntegerField(verbose_name='Скидка', null=True, blank=True)
    image = models.ImageField(upload_to='shops/sales', verbose_name='Изображение', null=True, blank=True)
    image_thumb = models.ImageField(upload_to='shops/sales/thumb', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (self.image and not self.pk) or (self.image and self.image != self.current_img):
            self.create_thumbnail()

        super().save(force_insert, force_update, using, update_fields)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_img = self.image

    def __str__(self):
        return self.title

    def create_thumbnail(self):
        create_thumbnail_image(main_image=self.image, thumb_image=self.image_thumb, thumbnail_size=(480, 480))
