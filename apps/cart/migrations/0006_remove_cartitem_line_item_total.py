# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-04 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cartitem_line_item_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='line_item_total',
        ),
    ]