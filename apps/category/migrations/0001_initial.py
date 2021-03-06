# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-01 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('global_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('published', models.BooleanField(default=True, verbose_name='Публиковать')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('image', models.FileField(blank=True, null=True, upload_to='category/icons/', verbose_name='Иконка категории')),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Название на транслите')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Очередь')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Category', verbose_name='Родительская категория')),
                ('section', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='global_category.GlobalCategory', verbose_name='Раздел')),
            ],
            options={
                'verbose_name_plural': 'Категории',
                'ordering': ['-updated_at'],
                'verbose_name': 'Категория',
            },
        ),
    ]
