# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0002_auto_20150218_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequence',
            name='webpage',
            field=models.ForeignKey(blank=True, to='website_management.Webpage', null=True),
            preserve_default=True,
        ),
    ]
