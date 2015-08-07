# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0005_auto_20150801_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webpage',
            name='full_url',
        ),
    ]
