# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-06 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cstasker', '0019_auto_20180606_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertask',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usertask',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usertask',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cstasker.Photo'),
        ),
    ]
