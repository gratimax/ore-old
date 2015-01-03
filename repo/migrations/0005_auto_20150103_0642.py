# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0004_populate_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationteam',
            name='name',
            field=models.CharField(max_length=80, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permission',
            name='slug',
            field=models.SlugField(max_length=64, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='name',
            field=models.CharField(max_length=80, verbose_name='name'),
            preserve_default=True,
        ),
    ]
