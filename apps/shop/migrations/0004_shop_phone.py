# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_shop_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='phone',
            field=models.CharField(default='', max_length=20, verbose_name='Телефон'),
        ),
    ]