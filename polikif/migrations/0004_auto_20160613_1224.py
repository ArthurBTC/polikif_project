# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-13 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polikif', '0003_historicalparti'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalparti',
            name='memberCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parti',
            name='memberCount',
            field=models.IntegerField(default=0),
        ),
    ]
