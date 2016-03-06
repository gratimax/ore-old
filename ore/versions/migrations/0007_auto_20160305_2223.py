# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-05 22:23
from __future__ import unicode_literals

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('versions', '0006_auto_20160214_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='unpublished', max_length=100, no_check_for_status=True),
        ),
        migrations.AlterField(
            model_name='version',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='unpublished', max_length=100, no_check_for_status=True),
        ),
    ]