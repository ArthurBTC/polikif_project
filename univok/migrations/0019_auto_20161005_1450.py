# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-05 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univok', '0018_auto_20161005_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='proposition',
            field=models.ManyToManyField(to='gdpcore.Proposition'),
        ),
    ]
