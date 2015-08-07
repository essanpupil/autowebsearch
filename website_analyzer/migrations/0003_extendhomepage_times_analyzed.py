# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0002_extendhomepage_full_crawled'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendhomepage',
            name='times_analyzed',
            field=models.IntegerField(default=0),
        ),
    ]
