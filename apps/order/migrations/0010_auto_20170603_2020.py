# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-03 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_cart_completed'),
        ('order', '0009_simpleorder_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simpleorder',
            name='products',
        ),
        migrations.RemoveField(
            model_name='simpleorder',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='simpleorder',
            name='subtotal',
        ),
        migrations.AddField(
            model_name='simpleorder',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart'),
        ),
    ]
