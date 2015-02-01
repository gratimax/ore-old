# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import ore.core.util


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid team name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('is_owner_team', models.BooleanField(default=False)),
                ('is_all_projects', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(to='ore.core.Organization', related_name='teams')),
                ('permissions', models.ManyToManyField(blank=True, to='ore.core.Permission', related_name='+')),
                ('projects', models.ManyToManyField(blank=True, to='ore.projects.Project', related_name='organizationteams')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='organizationteams')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid team name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('is_owner_team', models.BooleanField(default=False)),
                ('permissions', models.ManyToManyField(blank=True, to='ore.core.Permission', related_name='+')),
                ('project', models.ForeignKey(to='ore.projects.Project', related_name='teams')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='projectteams')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='projectteam',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationteam',
            unique_together=set([('organization', 'name')]),
        ),
    ]
