# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0009_stringparameter_times_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenddomain',
            name='report_feature',
            field=models.BooleanField(default=False),
        ),
    ]
