# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-25 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gdpcore', '0012_auto_20160422_1149'),
        ('polikif', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='proposition',
            field=models.ForeignKey(default='default', on_delete=django.db.models.deletion.CASCADE, to='gdpcore.Proposition'),
            preserve_default=False,
        ),
    ]
