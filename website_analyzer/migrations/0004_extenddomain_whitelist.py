# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0003_extendhomepage_times_analyzed'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenddomain',
            name='whitelist',
            field=models.NullBooleanField(max_length=7, choices=[(True, b'YES'), (False, b'NO'), (None, b'UNKNOWN')]),
        ),
    ]
