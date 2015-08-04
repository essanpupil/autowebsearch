# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0003_auto_20150801_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='full_url',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
