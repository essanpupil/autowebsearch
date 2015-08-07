# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0009_webpage_full_url'),
        ('administrative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('query', models.OneToOneField(to='website_management.Query')),
            ],
        ),
    ]
