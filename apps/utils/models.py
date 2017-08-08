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
