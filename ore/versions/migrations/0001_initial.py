# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import ore.core.util
import ore.versions.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', model_utils.fields.StatusField(choices=[('active', 'active'), ('deleted', 'deleted')], max_length=100, no_check_for_status=True, default='active')),
                ('file', models.FileField(max_length=512, upload_to=ore.versions.models.file_upload)),
                ('file_name', models.CharField(max_length=512)),
                ('file_extension', models.CharField(max_length=12, verbose_name='extension')),
                ('file_size', models.PositiveIntegerField(null=True)),
                ('project', models.ForeignKey(related_name='files', to='projects.Project')),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', model_utils.fields.StatusField(choices=[('active', 'active'), ('deleted', 'deleted')], max_length=100, no_check_for_status=True, default='active')),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+([\\w.@+ -]*[\\w.@+-]+)?$', 'Enter a valid version name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('project', models.ForeignKey(related_name='versions', to='projects.Project')),
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
            field=models.ForeignKey(null=True, blank=True, to='versions.Version', related_name='files'),
            preserve_default=True,
        ),
    ]
