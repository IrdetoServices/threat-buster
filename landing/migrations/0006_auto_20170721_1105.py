# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('landing', '0005_auto_20170717_1041'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='surveyresults',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='surveyresult',
            name='answer',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
