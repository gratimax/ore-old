# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0014_auto_20150104_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='default_filetype',
            field=models.OneToOneField(related_name='+', to='repo.FileType', null=True),
            preserve_default=True,
        ),
    ]
