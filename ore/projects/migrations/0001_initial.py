# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import model_utils.fields
import ore.core.util


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', model_utils.fields.StatusField(max_length=100, default='active', no_check_for_status=True, choices=[('active', 'active'), ('deleted', 'deleted')])),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid project name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('namespace', models.ForeignKey(to='ore.core.Namespace', related_name='projects')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('namespace', 'name')]),
        ),
    ]
