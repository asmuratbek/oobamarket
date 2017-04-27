# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-27 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_globalcategory_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Название на транслите'),
        ),
    ]