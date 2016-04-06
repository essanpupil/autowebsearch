# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendWebsite',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('full_crawled', models.IntegerField(default=0)),
                ('times_analyzed', models.IntegerField(default=0)),
                ('scam', models.NullBooleanField(choices=[(True, 'YES'), (False, 'NO'), (None, 'UNKNOWN')], max_length=7)),
                ('inspected', models.BooleanField(default=False)),
                ('reported', models.BooleanField(default=False)),
                ('access', models.BooleanField(default=True)),
                ('whitelist', models.NullBooleanField(choices=[(True, 'YES'), (False, 'NO'), (None, 'UNKNOWN')], max_length=7)),
            ],
        ),
        migrations.RemoveField(
            model_name='extendhomepage',
            name='homepage',
        ),
        migrations.DeleteModel(
            name='ExtendHomepage',
        ),
    ]
