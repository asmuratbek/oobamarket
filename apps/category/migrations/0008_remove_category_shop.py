# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-30 05:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_category_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='shop',
        ),
    ]