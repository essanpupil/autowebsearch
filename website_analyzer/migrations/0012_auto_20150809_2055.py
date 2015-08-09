# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0011_auto_20150809_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stringparameter',
            name='target_analyze',
            field=models.CharField(default=b'text_body', max_length=10),
        ),
    ]
