# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0003_auto_20150220_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='webpage',
            field=models.ManyToManyField(to='website_management.Webpage', null=True, blank=True),
            preserve_default=True,
        ),
    ]
