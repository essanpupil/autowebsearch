# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('free', models.NullBooleanField()),
                ('domain', models.OneToOneField(to='website_management.Domain')),
            ],
        ),
        migrations.CreateModel(
            name='ExtendHomepage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scam', models.NullBooleanField(max_length=7, choices=[(True, b'YES'), (False, b'NO'), (None, b'UNKNOWN')])),
                ('inspected', models.BooleanField(default=False)),
                ('reported', models.BooleanField(default=False)),
                ('access', models.BooleanField(default=True)),
                ('whitelist', models.NullBooleanField(max_length=7, choices=[(True, b'YES'), (False, b'NO'), (None, b'UNKNOWN')])),
                ('homepage', models.OneToOneField(to='website_management.Homepage')),
            ],
        ),
        migrations.CreateModel(
            name='ExtendWebpage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_body', models.TextField(null=True, blank=True)),
                ('webpage', models.OneToOneField(to='website_management.Webpage')),
            ],
        ),
        migrations.CreateModel(
            name='Pieces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Searching',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('keyword', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now=True)),
                ('webpages', models.ForeignKey(to='website_management.Webpage')),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SequenceDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StringAnalysist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('find', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StringParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.CharField(unique=True, max_length=255)),
                ('definitive', models.BooleanField(default=False)),
                ('date_added', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='stringanalysist',
            name='parameter',
            field=models.ForeignKey(to='website_analyzer.StringParameter'),
        ),
        migrations.AddField(
            model_name='stringanalysist',
            name='webpage',
            field=models.ForeignKey(to='website_management.Webpage'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='description',
            field=models.ForeignKey(to='website_analyzer.SequenceDescription'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='token',
            field=models.ForeignKey(to='website_analyzer.Token'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='webpage',
            field=models.ForeignKey(blank=True, to='website_management.Webpage', null=True),
        ),
        migrations.AddField(
            model_name='pieces',
            name='token',
            field=models.ForeignKey(to='website_analyzer.Token'),
        ),
        migrations.AddField(
            model_name='pieces',
            name='webpage',
            field=models.ForeignKey(to='website_management.Webpage'),
        ),
    ]
