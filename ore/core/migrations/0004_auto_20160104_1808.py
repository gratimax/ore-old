# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-04 18:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import ore.core.models
import ore.core.util


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_populate_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namespace',
            name='name',
            field=models.CharField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.\\-_]+$', 'Names can only contain letters, numbers, underscores and hyphens.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='avatar_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=ore.core.models.organization_avatar_upload, verbose_name='Avatar'),
        ),
    ]
