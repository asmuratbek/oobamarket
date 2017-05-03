# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-29 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20170429_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociallinks',
            name='icon',
            field=models.CharField(choices=[('facebook', 'Facebook.com'), ('vk', 'Vk.com'), ('ok', 'Odnoklassniki.ru'), ('instagram', 'Instagram.com')], default=None, max_length=255, verbose_name='Выбор соц. иконки'),
        ),
    ]