# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stringparameter',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2015, 3, 4, 3, 9, 23, 92049, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
