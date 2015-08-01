# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('date_start', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('time_start', models.DateField(auto_now_add=True)),
                ('time_end', models.DateField(null=True, blank=True)),
                ('client', models.ForeignKey(default=None, to='administrative.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_start', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(null=True, blank=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ManyToManyField(to='administrative.Event', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ForeignKey(blank=True, to='administrative.Event', null=True)),
                ('homepage', models.OneToOneField(to='website_management.Homepage')),
            ],
        ),
    ]
