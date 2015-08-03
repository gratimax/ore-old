# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150623_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='oreuser',
            name='external_id',
            field=models.CharField(blank=True, max_length=64, default=None, null=True, unique=True),
        ),
    ]
