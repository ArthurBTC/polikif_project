# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-06 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('univok', '0005_sentence_proposition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentence',
            name='record',
        ),
        migrations.AddField(
            model_name='sentence',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='univok.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sentence',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sentence',
            name='speaker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='univok.Speaker'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sentence',
            name='text',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
