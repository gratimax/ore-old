# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20150809_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='listed',
            field=models.ManyToManyField(to='projects.Page', blank=True, related_name='listed_by'),
        ),
    ]
