# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import ore.core.util
import ore.core.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(
                    serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', model_utils.fields.StatusField(choices=[
                 ('active', 'active'), ('deleted', 'deleted')], max_length=100, no_check_for_status=True, default='active')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='name', validators=[django.core.validators.RegexValidator(
                    '^[\\w.@+-]+$', 'Enter a namespace organization name.', 'invalid'), ore.core.util.validate_not_prohibited])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('namespace_ptr', models.OneToOneField(parent_link=True, primary_key=True,
                                                       auto_created=True, to='core.Namespace', serialize=False)),
                ('avatar_image', models.ImageField(null=True, blank=True,
                                                   default=None, upload_to=ore.core.models.organization_avatar_upload)),
            ],
            options={
            },
            bases=('core.namespace',),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(
                    serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
