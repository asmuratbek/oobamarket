# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-28 12:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_favoriteproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Товар'),
        ),
    ]
