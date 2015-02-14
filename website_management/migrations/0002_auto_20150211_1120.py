# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='last_response',
            field=models.CharField(max_length=3, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='webpage',
            name='last_response_check',
            field=models.DateField(default=datetime.datetime(2015, 2, 11, 4, 20, 22, 140251, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
