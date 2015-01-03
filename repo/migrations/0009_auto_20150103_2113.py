# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0008_file_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_extension',
            field=models.CharField(verbose_name='extension', default='ERROR', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='file_size',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
    ]
