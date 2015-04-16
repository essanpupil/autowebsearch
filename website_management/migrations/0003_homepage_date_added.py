# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0002_remove_homepage_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2015, 3, 24, 13, 41, 0, 147262, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
