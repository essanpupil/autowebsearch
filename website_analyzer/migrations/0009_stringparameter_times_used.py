# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0008_stringparameter_target_analyze'),
    ]

    operations = [
        migrations.AddField(
            model_name='stringparameter',
            name='times_used',
            field=models.IntegerField(default=0),
        ),
    ]
