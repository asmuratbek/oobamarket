# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-29 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20171029_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='logo_thumb',
            field=models.ImageField(blank=True, null=True, upload_to='images/shop/thumb/'),
        ),
    ]
