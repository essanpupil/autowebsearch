# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0002_extendhomepage_full_crawled'),
        ('administrative', '0002_clientkeyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ForeignKey(blank=True, to='administrative.Event', null=True)),
                ('string_parameter', models.OneToOneField(to='website_analyzer.StringParameter')),
            ],
        ),
    ]
