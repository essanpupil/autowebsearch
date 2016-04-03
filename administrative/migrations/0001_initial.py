# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website_management', '__first__'),
        ('website_analyzer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('date_start', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('query', models.OneToOneField(to='website_analyzer.SearchKeywords')),
            ],
        ),
        migrations.CreateModel(
            name='ClientSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('client', models.ForeignKey(to='administrative.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('time_start', models.DateField(auto_now_add=True)),
                ('time_end', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(default=None, to='administrative.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date_start', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ManyToManyField(to='administrative.Event', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ForeignKey(blank=True, to='administrative.Event', null=True)),
                ('homepage', models.OneToOneField(to='website_management.Homepage')),
            ],
        ),
        migrations.AddField(
            model_name='clientsequence',
            name='event',
            field=models.ForeignKey(blank=True, to='administrative.Event', null=True),
        ),
        migrations.AddField(
            model_name='clientsequence',
            name='string_parameter',
            field=models.OneToOneField(to='website_analyzer.StringParameter'),
        ),
    ]
