# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_analyzer', '0002_auto_20160406_1944'),
        ('website_management', '0003_auto_20160406_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendwebsite',
            name='website',
            field=models.OneToOneField(to='website_management.Website'),
        ),
    ]
