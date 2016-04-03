# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


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
        ),
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('date_added', models.DateField(auto_now=True)),
                ('crawl_completed', models.BooleanField(default=False)),
                ('times_analyzed', models.IntegerField(default=0)),
                ('domain', models.ForeignKey(blank=True, to='website_management.Domain', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('url', models.URLField(unique=True, max_length=255)),
                ('full_url', models.TextField(default='', blank=True)),
                ('html_page', models.TextField(blank=True)),
                ('date_added', models.DateField(auto_now=True)),
                ('last_response', models.CharField(max_length=3, blank=True)),
                ('last_response_check', models.DateField(null=True, blank=True)),
                ('redirect_url', models.URLField(blank=True)),
                ('times_crawled', models.IntegerField(default=0)),
                ('homepage', models.ForeignKey(blank=True, to='website_management.Homepage', null=True)),
            ],
        ),
    ]
