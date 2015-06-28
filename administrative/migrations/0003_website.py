# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '__first__'),
        ('administrative', '0002_auto_20150628_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Event', models.ForeignKey(blank=True, to='administrative.Event', null=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('homepage', models.OneToOneField(to='website_management.Homepage')),
            ],
        ),
    ]
