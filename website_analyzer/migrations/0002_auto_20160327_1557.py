# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendwebpage',
            name='text_body',
            field=models.TextField(blank=True),
        ),
    ]
