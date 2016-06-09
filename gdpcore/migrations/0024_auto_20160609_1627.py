# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-09 14:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gdpcore', '0023_auto_20160526_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('creation_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gdpcore.Graph')),
            ],
        ),
        migrations.AlterField(
            model_name='proposition',
            name='nature',
            field=models.CharField(choices=[('Diagnostic', 'Diagnostic'), ('Action', 'Action'), ('Reference', 'Reference'), ('YT', 'Youtube'), ('SY', 'Syllogisme')], default='Diagnostic', max_length=30),
        ),
    ]
