# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-13 09:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polikif', '0002_selection_proposition'),
        ('gdpcore', '0026_graph_propnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalGraph',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('graphstring', models.CharField(default='', max_length=10000)),
                ('title', models.CharField(max_length=300)),
                ('originx', models.IntegerField(default=0)),
                ('originy', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField()),
                ('propNumber', models.IntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('autor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parti', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='polikif.Parti')),
            ],
            options={
                'verbose_name': 'historical graph',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
