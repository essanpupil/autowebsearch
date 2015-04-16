# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0004_auto_20150308_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendhomepage',
            name='reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='extendhomepage',
            name='scam',
            field=models.NullBooleanField(max_length=7, choices=[(True, b'YES'), (False, b'NO'), (None, b'UNKNOWN')]),
        ),
        migrations.AlterField(
            model_name='extendhomepage',
            name='whitelist',
            field=models.NullBooleanField(max_length=7, choices=[(True, b'YES'), (False, b'NO'), (None, b'UNKNOWN')]),
        ),
    ]
