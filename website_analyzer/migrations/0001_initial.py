# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0004_auto_20150216_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('free', models.NullBooleanField()),
                ('domain', models.OneToOneField(to='website_management.Domain')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtendHomepage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scam', models.NullBooleanField(max_length=10)),
                ('inspected', models.BooleanField(default=False)),
                ('reported', models.NullBooleanField()),
                ('access', models.BooleanField(default=True)),
                ('whitelist', models.NullBooleanField()),
                ('homepage', models.OneToOneField(to='website_management.Homepage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtendWebpage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('webpage', models.OneToOneField(to='website_management.Webpage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='searching',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('keyword', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now=True)),
                ('webpages', models.ForeignKey(to='website_management.Webpage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='sequence',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('number', models.IntegerField()),
                ('description', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('webpage', models.ManyToManyField(to='website_management.Webpage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sequence',
            name='token',
            field=models.ForeignKey(to='website_analyzer.Token'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sequence',
            name='webpage',
            field=models.ForeignKey(to='website_management.Webpage'),
            preserve_default=True,
        ),
    ]
