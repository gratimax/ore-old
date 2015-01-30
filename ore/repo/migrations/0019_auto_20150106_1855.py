# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0018_auto_20150107_0125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='default_filetype',
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='filetype',
            name='project',
        ),
        migrations.RemoveField(
            model_name='file',
            name='filetype',
        ),
        migrations.DeleteModel(
            name='FileType',
        ),
        migrations.AddField(
            model_name='file',
            name='project',
            field=models.ForeignKey(default=None, to='ore.repo.Project', related_name='files'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file',
            name='version',
            field=models.ForeignKey(to='ore.repo.Version', related_name='files', blank=True, null=True),
            preserve_default=True,
        ),
    ]
