# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-28 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop', verbose_name='Магазин'),
        ),
    ]