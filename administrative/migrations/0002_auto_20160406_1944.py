# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientWebsite',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('client', models.ForeignKey(to='administrative.Client')),
                ('event', models.ForeignKey(blank=True, null=True, to='administrative.Event')),
            ],
        ),
        migrations.RemoveField(
            model_name='website',
            name='client',
        ),
        migrations.RemoveField(
            model_name='website',
            name='event',
        ),
        migrations.RemoveField(
            model_name='website',
            name='homepage',
        ),
        migrations.DeleteModel(
            name='Website',
        ),
    ]
