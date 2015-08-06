# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0004_extenddomain_whitelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenddomain',
            name='times_crawled',
            field=models.IntegerField(default=0),
        ),
    ]
