# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0013_auto_20170319_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due',
            field=models.DateField(blank=True, default='datetime.datetime.now()'),
        ),
    ]
