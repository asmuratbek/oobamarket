# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-04 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_auto_20170705_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='category',
            field=models.ManyToManyField(blank=True, to='category.Category', verbose_name='Категория'),
        ),
    ]