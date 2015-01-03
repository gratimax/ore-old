# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import repo.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0005_auto_20150103_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='avatar_image',
            field=models.ImageField(default=None, null=True, upload_to=repo.models.organization_avatar_upload, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationteam',
            name='permissions',
            field=models.ManyToManyField(related_name='+', to='repo.Permission', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationteam',
            name='projects',
            field=models.ManyToManyField(related_name='organizationteams', to='repo.Project', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationteam',
            name='users',
            field=models.ManyToManyField(related_name='organizationteams', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='permissions',
            field=models.ManyToManyField(related_name='+', to='repo.Permission', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='users',
            field=models.ManyToManyField(related_name='projectteams', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
