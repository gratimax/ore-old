# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0015_auto_20150104_0859'),
    ]

    operations = [
    	migrations.AlterField(
            model_name='flag',
            name='resolver',
            field=models.ForeignKey(blank=True, null=True, related_name='resolver_flags', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
