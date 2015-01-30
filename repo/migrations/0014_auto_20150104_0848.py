# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0013_auto_20150104_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='description',
        ),
        migrations.RemoveField(
            model_name='file',
            name='name',
        ),
    ]
