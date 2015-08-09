# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website_management', '0009_webpage_full_url'),
        ('administrative', '0003_clientsequence'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_time', models.DateTimeField(auto_now_add=True)),
                ('homepage', models.ForeignKey(to='website_management.Homepage')),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
