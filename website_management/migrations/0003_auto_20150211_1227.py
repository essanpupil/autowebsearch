# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0002_auto_20150211_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='url',
            field=models.URLField(unique=True, max_length=250),
            preserve_default=True,
        ),
    ]
