# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('administrative', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date_end',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2015, 6, 28, 4, 25, 12, 76298, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
