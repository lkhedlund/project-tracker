# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='count',
            name='count_update',
            field=models.IntegerField(default=0),
        ),
    ]
