# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0005_extenddomain_times_crawled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stringanalysist',
            name='time',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
