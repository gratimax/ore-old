# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-04 22:35
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import Func


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_namespace_lower_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namespace',
            name='lower_name',
            field=models.CharField(blank=True, max_length=32, unique=True, verbose_name='name'),
        ),
    ]