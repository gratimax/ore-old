# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import ore.core.util


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationTeam',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid team name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('is_owner_team', models.BooleanField(default=False)),
                ('is_all_projects', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='teams', to='core.Organization')),
                ('permissions', models.ManyToManyField(blank=True, related_name='+', to='core.Permission')),
                ('projects', models.ManyToManyField(blank=True, related_name='organizationteams', to='projects.Project')),
                ('users', models.ManyToManyField(blank=True, related_name='organizationteams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=80, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid team name.', 'invalid'), ore.core.util.validate_not_prohibited], verbose_name='name')),
                ('is_owner_team', models.BooleanField(default=False)),
                ('permissions', models.ManyToManyField(blank=True, related_name='+', to='core.Permission')),
                ('project', models.ForeignKey(related_name='teams', to='projects.Project')),
                ('users', models.ManyToManyField(blank=True, related_name='projectteams', to=settings.AUTH_USER_MODEL)),
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
