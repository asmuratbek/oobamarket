# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-10 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(verbose_name='Полное описание магазина'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='short_description',
            field=models.TextField(verbose_name='Короткое описание магазина'),
        ),
    ]
