# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-18 14:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20170510_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='updated_ad',
            new_name='updated_at',
        ),
    ]