# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 10:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('landing', '0004_auto_20170714_1150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenant',
            options={'permissions': (('view_tenant', 'View tenant'),), 'verbose_name': 'tenant',
                     'verbose_name_plural': 'tenants'},
        ),
    ]