# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-01 09:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Администратор магазина'),
        ),
        migrations.AddField(
            model_name='sales',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Place', verbose_name='Торговая точка'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='banners',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
    ]
