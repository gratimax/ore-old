# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ore.repo.models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0007_project_rename_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default='ERROR', upload_to=ore.repo.models.file_upload),
            preserve_default=False,
        ),
    ]
