# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-19 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cstasker', '0005_question_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.TextField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tel',
            field=models.TextField(blank=True, max_length=11, null=True),
        ),
    ]
