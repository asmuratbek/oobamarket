# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-22 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20170821_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='thumb_image',
            field=models.ImageField(height_field=200, max_length=230, null=True, upload_to='products/image/thumb', width_field=200),
        ),
    ]
