# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-27 07:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20170518_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociallinks',
            name='facebook',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='sociallinks',
            name='instagram',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='sociallinks',
            name='twitter',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Twitter'),
        ),
        migrations.AddField(
            model_name='sociallinks',
            name='vk',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='VK'),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='shop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
    ]
