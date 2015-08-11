# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0009_webpage_full_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='times_analyzed',
            field=models.IntegerField(default=0),
        ),
    ]
