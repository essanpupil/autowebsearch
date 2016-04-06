# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='id',
            field=models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='id',
            field=models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='webpage',
            name='id',
            field=models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True),
        ),
    ]
