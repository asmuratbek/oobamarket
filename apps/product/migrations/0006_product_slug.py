# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20170427_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Название на транслите'),
        ),
    ]
