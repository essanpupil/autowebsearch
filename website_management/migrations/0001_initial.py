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
                ('name', models.CharField(max_length=75, unique=True)),
                ('date_added', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('date_added', models.DateField(auto_now=True)),
                ('crawl_completed', models.BooleanField(default=False)),
                ('domain', models.ForeignKey(null=True, to='website_management.Domain', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('keywords', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('times_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('search_time', models.DateTimeField(auto_now=True)),
                ('query', models.ForeignKey(to='website_management.Query')),
            ],
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('url', models.URLField(max_length=255, unique=True)),
                ('full_url', models.TextField(null=True, blank=True, default='')),
                ('html_page', models.TextField(null=True, blank=True)),
                ('date_added', models.DateField(auto_now=True)),
                ('last_response', models.CharField(max_length=3, null=True, blank=True)),
                ('last_response_check', models.DateField(null=True, blank=True)),
                ('redirect_url', models.URLField(null=True, blank=True)),
                ('times_crawled', models.IntegerField(default=0)),
                ('homepage', models.ForeignKey(null=True, to='website_management.Homepage', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='search',
            name='webpage',
            field=models.ForeignKey(to='website_management.Webpage'),
        ),
    ]
