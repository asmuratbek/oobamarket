# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-27 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_shop_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacts',
            name='contact_type',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='contact_value',
        ),
        migrations.AddField(
            model_name='contacts',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Place', verbose_name='Торговая точка'),
        ),
    ]
