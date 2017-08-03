# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-01 13:53
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20170801_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='shops/sales', verbose_name='Изображение'),
        ),
    ]