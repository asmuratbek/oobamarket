# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-13 06:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleorder',
            name='status',
            field=models.CharField(choices=[('created', 'Новый'), ('processed', 'Обработан'), ('shipped', 'Доставлен'), ('paid', 'Оплачен'), ('refunded', 'Отказан')], default='created', max_length=120),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Новый'), ('processed', 'Обработан'), ('shipped', 'Доставлен'), ('paid', 'Оплачен'), ('refunded', 'Отказан')], default='created', max_length=120),
        ),
    ]
