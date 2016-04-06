# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0002_auto_20160406_1944'),
        ('administrative', '0002_auto_20160406_1944'),
        ('website_management', '0002_auto_20160406_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('date_added', models.DateField(auto_now=True)),
                ('crawl_completed', models.BooleanField(default=False)),
                ('times_analyzed', models.IntegerField(default=0)),
                ('domain', models.ForeignKey(blank=True, null=True, to='website_management.Domain')),
            ],
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='domain',
        ),
        migrations.AlterField(
            model_name='webpage',
            name='homepage',
            field=models.ForeignKey(blank=True, null=True, to='website_management.Website'),
        ),
        migrations.DeleteModel(
            name='Homepage',
        ),
    ]
