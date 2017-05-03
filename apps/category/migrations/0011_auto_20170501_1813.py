# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-01 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_auto_20170501_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='section',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='global_category.GlobalCategory', verbose_name='Раздел'),
        ),
    ]