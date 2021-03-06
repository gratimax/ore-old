# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 12:47
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    ProjectTeam = apps.get_model('teams', 'ProjectTeam')
    Permission = apps.get_model('core', 'Permission')
    owner_teams = ProjectTeam.objects.filter(
        is_owner_team=True
    )
    for owner_team in owner_teams:
        if owner_team.users.count() == 1:
            owner_team.delete()
        else:
            owner_team.is_owner_team = False
            owner_team.permissions = Permission.objects.filter(
                applies_to_model__model='ProjectTeam'
            )
            owner_team.save()


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20160105_1952'),
        ('core', '0007_auto_20160105_0431'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func
        )
    ]
