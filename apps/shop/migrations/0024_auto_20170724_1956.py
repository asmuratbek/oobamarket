# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-24 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_remove_contacts_work_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='round_the_clock',
            field=models.BooleanField(default=False, verbose_name='Круглосуточно'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='friday',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Пятница'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='saturday',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Суббота'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='sunday',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Воскресенье'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='thursday',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Четверг'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='tuesday',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Вторник'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='wednesday',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Среда'),
        ),
    ]
