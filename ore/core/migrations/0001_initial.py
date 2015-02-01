# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.core.validators
import ore.core.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', model_utils.fields.StatusField(max_length=100, default='active', no_check_for_status=True, choices=[('active', 'active'), ('deleted', 'deleted')])),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a namespace organization name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('namespace_ptr', models.OneToOneField(auto_created=True, to='ore.core.Namespace', serialize=False, parent_link=True, primary_key=True)),
                ('avatar_image', models.ImageField(blank=True, upload_to=ore.core.models.organization_avatar_upload, default=None, null=True)),
            ],
            options={
            },
            bases=('core.namespace',),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('applies_to_project', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
