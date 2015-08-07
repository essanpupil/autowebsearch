# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0006_remove_webpage_full_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='full_url',
            field=models.TextField(null=True, blank=True),
        ),
    ]
