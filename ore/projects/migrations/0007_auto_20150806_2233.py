# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150804_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='html',
            field=models.TextField(blank=True),
        ),
    ]
