# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-10 05:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_auto_20170609_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_at',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]