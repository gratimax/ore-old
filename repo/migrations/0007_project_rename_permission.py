# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

PROJECT_PERMISSIONS = [
        ('project.rename', 'Change a project\'s name')
]
ORGANIZATION_PERMISSIONS = [
]

def forwards_func(apps, schema_editor):
    Permission = apps.get_model("repo", "Permission")
    for slug, name in PROJECT_PERMISSIONS:
        Permission.objects.create(slug=slug, name=name, description='', applies_to_project=True)
    for slug, name in ORGANIZATION_PERMISSIONS:
        Permission.objects.create(slug=slug, name=name, description='', applies_to_project=False)


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0006_auto_20150103_1654'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
