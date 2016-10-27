# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-26 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gdpcore', '0038_showpart_synthese'),
        ('univok', '0024_speaker_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='show2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='show2', to='gdpcore.Show'),
        ),
        migrations.AlterField(
            model_name='event',
            name='show',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='show', to='gdpcore.Show'),
        ),
    ]
