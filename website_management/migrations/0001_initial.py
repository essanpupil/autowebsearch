# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=75)),
                ('date_added', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('date_added', models.DateField(auto_now=True)),
                ('domain', models.ForeignKey(blank=True, to='website_management.Domain', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('url', models.URLField(unique=True, max_length=250, blank=True)),
                ('html_page', models.TextField(null=True, blank=True)),
                ('date_added', models.DateField(auto_now=True)),
                ('homepage', models.ForeignKey(blank=True, to='website_management.Homepage', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
