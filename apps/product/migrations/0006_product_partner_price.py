# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-03 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20170803_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='partner_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Цена для партнера'),
        ),
    ]
