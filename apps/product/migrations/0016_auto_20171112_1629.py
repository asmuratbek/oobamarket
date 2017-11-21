# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-12 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=2, max_digits=2, verbose_name='Курс'),
        ),
    ]