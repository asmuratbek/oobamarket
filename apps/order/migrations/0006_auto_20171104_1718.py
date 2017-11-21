# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-04 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20171029_1844'),
        ('order', '0005_simpleorder_confirm_shops'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleorder',
            name='rejected_shops',
            field=models.ManyToManyField(related_name='rejected_shops', to='shop.Shop', verbose_name='Отклоненные магазины'),
        ),
        migrations.AlterField(
            model_name='simpleorder',
            name='confirm_shops',
            field=models.ManyToManyField(related_name='confirm_shops', to='shop.Shop', verbose_name='Подтвержденные магазины'),
        ),
    ]