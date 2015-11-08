# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0009_auto_20150901_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='stargazers',
            field=models.ManyToManyField(related_name='starred', to=settings.AUTH_USER_MODEL),
        ),
    ]
