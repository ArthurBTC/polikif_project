# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 15:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gdpcore', '0007_auto_20160413_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Implication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gdpcore.Link')),
                ('proposition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gdpcore.Proposition')),
            ],
        ),
        migrations.AlterField(
            model_name='notification',
            name='nature',
            field=models.CharField(choices=[('Reponse', 'Reponse'), ('Demande', 'Demande'), ("Demande d'attention", "Demande d'attention"), ('Demande de précision', 'Demande de précision'), ('Demande de source', 'Demande de source'), ('DA', "Demande d'attention"), ('DP', 'Demande de précision'), ('DS', 'Demande de source')], default='Reponse', max_length=30),
        ),
    ]
