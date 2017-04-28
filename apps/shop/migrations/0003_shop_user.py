# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-28 10:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_auto_20170427_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Администратор магазина'),
        ),
    ]
