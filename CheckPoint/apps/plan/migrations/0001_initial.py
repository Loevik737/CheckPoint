# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Objectives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_objective', models.TextField(blank=True, max_length=200)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_objectives', to='subject.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('term', models.CharField(max_length=10, verbose_name='Semester')),
                ('year', models.IntegerField(default=2017)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='subject.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.IntegerField(blank=True, verbose_name='Ukenummer')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to='plan.Plan')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='objectives',
            field=models.ManyToManyField(to='plan.Objectives'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='plan.Plan'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='plan.Week'),
        ),
    ]
