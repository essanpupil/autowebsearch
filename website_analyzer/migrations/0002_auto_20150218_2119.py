# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendhomepage',
            name='scam',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
