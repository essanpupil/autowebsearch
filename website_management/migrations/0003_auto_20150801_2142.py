# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0002_query_times_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='url',
            field=models.URLField(unique=True, max_length=255),
        ),
    ]
