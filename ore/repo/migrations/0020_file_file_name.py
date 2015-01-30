# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0019_auto_20150106_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_name',
            field=models.CharField(max_length=512, default=None),
            preserve_default=False,
        ),
    ]
