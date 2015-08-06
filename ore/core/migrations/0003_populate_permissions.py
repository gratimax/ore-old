# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

permissions = [
    ("version.create",      "Create new versions",                                      "project"),
    ("version.edit",        "Edit versions",                                            "project"),
    ("version.delete",      "Delete versions",                                          "project"),
    ("file.create",         "Upload new files",                                         "project"),
    ("file.edit",           "Edit files",                                               "project"),
    ("file.delete",         "Delete files",                                             "project"),
    ("project.edit",        "Edit a project",                                           "project"),
    ("project.rename",      "Change a project's name",                                  "project"),
    ("project.transfer",    "Transfer a project to a different user or organization",   "project"),
    ("project.delete",      "Delete a project",                                         "project"),
    ("project.team.create", "Create a new project team",                                "project"),
    ("project.team.delete", "Delete a project team",                                    "project"),
    ("project.team.edit",   "Edit a project team's name or description",                "project"),
    ("project.team.manage", "Manage the members of a project team",                     "project"),
    ("org.project.create",  "Create a new project under an organization",               "organization"),
    ("org.team.create",     "Create a new organization team",                           "organization"),
    ("org.team.edit",       "Edit a organization team's name or description",           "organization"),
    ("org.team.manage",     "Manage the members of an organization team",               "organization"),
    ("org.team.delete",     "Delete an organization team",                              "organization"),
]

def forwards_func(apps, schema_editor):
    Permission = apps.get_model('core', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    project_content_type = ContentType.objects.get_for_model(apps.get_model('projects', 'Project'))
    organization_content_type = ContentType.objects.get_for_model(apps.get_model('core', 'Organization'))

    content_type_mapper = {
        'project': project_content_type,
        'organization': organization_content_type
    }

    for (slug, name, applies_to_model) in permissions:
        perm = Permission(slug=slug, name=name, applies_to_model=content_type_mapper[applies_to_model])
        perm.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150804_1818'),
        ('projects', '0002_auto_20150624_0445'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func
        )
    ]
