# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrative', '0003_website'),
    ]

    operations = [
        migrations.RenameField(
            model_name='website',
            old_name='Event',
            new_name='event',
        ),
    ]
