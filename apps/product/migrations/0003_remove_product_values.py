# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-11 13:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20170610_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='values',
        ),
    ]
