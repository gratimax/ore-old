# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='applies_to_project',
        ),
        migrations.AddField(
            model_name='permission',
            name='applies_to_model',
            field=models.ForeignKey(related_name='ore_permissions', default=5, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
    ]
