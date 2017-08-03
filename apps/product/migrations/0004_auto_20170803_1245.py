# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-03 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_favoriteproduct_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='delivery_type',
            field=models.CharField(blank=True, choices=[('self', 'Самовывоз'), ('paid', 'Платная доставка'), ('free', 'Бесплатная доставка')], max_length=255, null=True, verbose_name='Вид доставки'),
        ),
    ]
