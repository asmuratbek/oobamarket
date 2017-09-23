from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Обновлено'))

    objects = models.Manager()

    class Meta:
        abstract = True


class PublishBaseModel(BaseModel):
    published = models.BooleanField(_('Публиковать'), default=True)

    class Meta:
        abstract = True


class Counter(models.Model):
    counter = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)

    class Meta:
        abstract = True


class MetaBaseModel(models.Model):
    meta_title = models.CharField(max_length=60, verbose_name='Мета заголовок', blank=True, null=True)
    meta_description = models.CharField(max_length=255, verbose_name='Мета описание', blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, verbose_name='Мета ключевые слова', blank=True, null=True)
    seo_text = models.TextField(verbose_name='SEO Текст', null=True, blank=True)

    class Meta:
        abstract = True


class PostionMapModel(models.Model):
    latitude = models.CharField(max_length=255, verbose_name='Широта', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='Долгота', null=True, blank=True)

    class Meta:
        abstract = True
