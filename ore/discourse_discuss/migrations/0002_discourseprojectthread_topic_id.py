# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourse_discuss', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discourseprojectthread',
            name='topic_id',
            field=models.PositiveIntegerField(default=10741),
            preserve_default=False,
        ),
    ]
