# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 08:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20170429_1411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='short_decription',
            new_name='short_description',
        ),
    ]
