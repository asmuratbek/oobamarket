# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-22 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20170825_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='latitude',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Широта'),
        ),
        migrations.AddField(
            model_name='place',
            name='longitude',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Долгота'),
        ),
    ]
