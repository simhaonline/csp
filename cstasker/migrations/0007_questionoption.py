# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-19 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cstasker', '0006_auto_20180419_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, max_length=255, null=True)),
                ('q_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cstasker.Question')),
            ],
        ),
    ]