# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='full_url',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='html_page',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='last_response',
            field=models.CharField(max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='redirect_url',
            field=models.URLField(blank=True),
        ),
    ]
