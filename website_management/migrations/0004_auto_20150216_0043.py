# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0003_auto_20150211_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='last_response_check',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
