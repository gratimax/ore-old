# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import repo.models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0011_auto_20150104_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(max_length=512, upload_to=repo.models.file_upload),
            preserve_default=True,
        ),
    ]
