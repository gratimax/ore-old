# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_channels(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Channel = apps.get_model('projects', 'Channel')
    db_alias = schema_editor.connection.alias
    projects = Project.objects.using(db_alias).all()
    for proj in projects:
        Channel(name='Stable', hex='2ECC40', project=proj).save(using=db_alias)
        Channel(name='Beta', hex='0074D9', project=proj).save(using=db_alias)

def delete_channels(apps, schema_editor):
    Channel = apps.get_model('projects', 'Channel')
    db_alias = schema_editor.connection.alias
    Channel.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_project_stargazers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('hex', models.CharField(max_length=6)),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
        ),
        migrations.RunPython(create_channels, delete_channels)
    ]
