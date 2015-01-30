# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ore.repo.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0015_auto_20150104_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repouser',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='namespace',
            name='name',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a namespace organization name.', 'invalid'), ore.repo.models.validate_not_prohibited], verbose_name='name', max_length=32, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationteam',
            name='name',
            field=models.CharField(verbose_name='name', max_length=80, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid team name.', 'invalid'), ore.repo.models.validate_not_prohibited]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(verbose_name='name', max_length=32, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid project name.', 'invalid'), ore.repo.models.validate_not_prohibited]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='name',
            field=models.CharField(verbose_name='name', max_length=80, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid team name.', 'invalid'), ore.repo.models.validate_not_prohibited]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='name',
            field=models.CharField(verbose_name='name', max_length=32, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+([\\w.@+ -]*[\\w.@+-]+)?$', 'Enter a valid version name.', 'invalid'), ore.repo.models.validate_not_prohibited]),
            preserve_default=True,
        ),
    ]
