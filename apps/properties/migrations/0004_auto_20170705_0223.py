# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-04 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_auto_20170703_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Очередь'),
        ),
        migrations.AlterField(
            model_name='properties',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properties.Properties', verbose_name='Родительская категория'),
        ),
        migrations.AlterField(
            model_name='values',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Очередь'),
        ),
    ]
