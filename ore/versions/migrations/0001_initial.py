# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.core.validators
import ore.versions.models

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', model_utils.fields.StatusField(max_length=100, default='active', no_check_for_status=True, choices=[('active', 'active'), ('deleted', 'deleted')])),
                ('file', models.FileField(max_length=512, upload_to=ore.versions.models.file_upload)),
                ('file_name', models.CharField(max_length=512)),
                ('file_extension', models.CharField(max_length=12, verbose_name='extension')),
                ('file_size', models.PositiveIntegerField(null=True)),
                ('project', models.ForeignKey(to='ore.projects.Project', related_name='files')),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', model_utils.fields.StatusField(max_length=100, default='active', no_check_for_status=True, choices=[('active', 'active'), ('deleted', 'deleted')])),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+([\\w.@+ -]*[\\w.@+-]+)?$', 'Enter a valid version name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('project', models.ForeignKey(to='ore.projects.Project', related_name='versions')),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AddField(
            model_name='file',
            name='version',
            field=models.ForeignKey(to='ore.versions.Version', null=True, blank=True, related_name='files'),
            preserve_default=True,
        ),
    ]
