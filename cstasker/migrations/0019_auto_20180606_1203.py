# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-06 04:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cstasker', '0018_auto_20180527_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUsageLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('log', models.TextField(max_length=255)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.IntegerField(choices=[(0, 'LocationBased'), (1, 'TimeSensitive')]),
        ),
    ]
