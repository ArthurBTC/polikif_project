# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-06 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdn', '0004_member_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='presence',
            name='status',
            field=models.CharField(default='default', max_length=100),
        ),
    ]
