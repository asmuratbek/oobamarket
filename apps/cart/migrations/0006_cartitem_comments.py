# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-09 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20170803_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарии к продукту'),
        ),
    ]
