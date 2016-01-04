# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_channel'),
        ('versions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='channel',
            field=models.ForeignKey(default=1, to='projects.Channel'),
            preserve_default=False,
        ),
    ]
