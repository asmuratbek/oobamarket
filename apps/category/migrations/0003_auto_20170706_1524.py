# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-06 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.FileField(null=True, upload_to='category/icons/', verbose_name='Иконка категории'),
        ),
    ]