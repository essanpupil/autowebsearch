# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website_analyzer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('query', models.OneToOneField(to='website_management.Query')),
            ],
        ),
        migrations.CreateModel(
            name='ClientSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('client', models.ForeignKey(to='administrative.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('time_start', models.DateField(auto_now_add=True)),
                ('time_end', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(to='administrative.Client', default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date_start', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ManyToManyField(blank=True, to='administrative.Event')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
