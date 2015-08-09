# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20150806_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='listed',
            field=models.ManyToManyField(to='projects.Page', related_name='listed_by'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='page',
            order_with_respect_to=None,
        ),
        migrations.RemoveField(
            model_name='page',
            name='parent',
        ),
    ]
