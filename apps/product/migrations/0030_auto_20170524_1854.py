# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-24 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_auto_20170524_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='/images')),
            ],
            options={
                'verbose_name_plural': 'Изображения',
                'verbose_name': 'Изображение',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, to='product.Media', verbose_name='Изображения продукта'),
        ),
    ]
