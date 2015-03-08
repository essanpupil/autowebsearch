# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0003_auto_20150304_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stringparameter',
            name='level',
        ),
        migrations.AddField(
            model_name='stringparameter',
            name='definitive',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
