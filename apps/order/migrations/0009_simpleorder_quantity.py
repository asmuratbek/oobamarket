# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-03 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_simpleorder_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleorder',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
