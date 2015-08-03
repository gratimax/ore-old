# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import ore.core.util
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(
                    serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', model_utils.fields.StatusField(choices=[
                 ('active', 'active'), ('deleted', 'deleted')], max_length=100, no_check_for_status=True, default='active')),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator(
                    '^[\\w.@+-]+$', 'Enter a valid project name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('namespace', models.ForeignKey(
                    related_name='projects', to='core.Namespace')),
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
