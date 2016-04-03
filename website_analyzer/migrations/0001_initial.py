# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0002_auto_20160327_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('whitelist', models.NullBooleanField(max_length=7, choices=[(True, 'YES'), (False, 'NO'), (None, 'UNKNOWN')])),
                ('free', models.NullBooleanField()),
                ('times_crawled', models.IntegerField(default=0)),
                ('report_feature', models.BooleanField(default=False)),
                ('domain', models.OneToOneField(to='website_management.Domain')),
            ],
        ),
        migrations.CreateModel(
            name='ExtendHomepage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('full_crawled', models.IntegerField(default=0)),
                ('times_analyzed', models.IntegerField(default=0)),
                ('scam', models.NullBooleanField(max_length=7, choices=[(True, 'YES'), (False, 'NO'), (None, 'UNKNOWN')])),
                ('inspected', models.BooleanField(default=False)),
                ('reported', models.BooleanField(default=False)),
                ('access', models.BooleanField(default=True)),
                ('whitelist', models.NullBooleanField(max_length=7, choices=[(True, 'YES'), (False, 'NO'), (None, 'UNKNOWN')])),
                ('homepage', models.OneToOneField(to='website_management.Homepage')),
            ],
        ),
        migrations.CreateModel(
            name='ExtendWebpage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text_body', models.TextField(blank=True)),
                ('webpage', models.OneToOneField(to='website_management.Webpage')),
            ],
        ),
        migrations.CreateModel(
            name='Pieces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Searching',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchKeywords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('keywords', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('times_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SequenceDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StringAnalysist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True, db_index=True)),
                ('find', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StringParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sentence', models.CharField(max_length=255, unique=True)),
                ('definitive', models.BooleanField(default=False)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('target_analyze', models.CharField(max_length=10, default='text_body')),
                ('times_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
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
            field=models.ForeignKey(to='website_management.Webpage', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='searching',
            name='keyword',
            field=models.ForeignKey(to='website_analyzer.SearchKeywords'),
        ),
        migrations.AddField(
            model_name='searching',
            name='webpages',
            field=models.ForeignKey(to='website_management.Webpage'),
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
