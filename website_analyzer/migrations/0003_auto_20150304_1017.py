# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0002_stringparameter_date_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stringparameter',
            old_name='name',
            new_name='sentence',
        ),
    ]
