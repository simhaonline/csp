# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-19 03:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cstasker', '0004_auto_20180419_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]