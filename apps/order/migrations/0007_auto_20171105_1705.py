# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-05 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20171104_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleorder',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart'),
        ),
    ]
