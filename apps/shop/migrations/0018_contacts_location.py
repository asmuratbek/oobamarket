# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-12 12:18
from __future__ import unicode_literals

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20170712_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='location',
            field=geoposition.fields.GeopositionField(blank=True, max_length=42, null=True, verbose_name='Отметьте на карте'),
        ),
    ]
