# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def set_channel_default(apps, schema_editor):
    Version = apps.get_model('versions', 'Version')
    Channel = apps.get_model('projects', 'Channel')
    db_alias = schema_editor.connection.alias
    versions = Version.objects.using(db_alias).filter(channel=None)
    for version in versions:
        version.channel = Channel.objects.using(db_alias).get(project=version.project, name="Stable")
        version.save(using=db_alias)

def remove_channel_default(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_channel'),
        ('versions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='channel',
            field=models.ForeignKey(null=True, default=None, to='projects.Channel'),
            preserve_default=False,
        ),
        migrations.RunPython(set_channel_default, remove_channel_default),
        migrations.AlterField(
            model_name='version',
            name='channel',
            field=models.ForeignKey(null=False, to='projects.Channel'),
            preserve_default=False,
        ),
    ]
