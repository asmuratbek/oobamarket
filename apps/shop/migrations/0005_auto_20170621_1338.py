# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20170615_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop', verbose_name='Магазин'),
        ),
    ]