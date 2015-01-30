# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0002_auto_20150103_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name=b'name')),
                ('is_owner_team', models.BooleanField(default=False)),
                ('is_all_projects', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='teams', to='ore.repo.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('applies_to_project', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name=b'name')),
                ('is_owner_team', models.BooleanField(default=False)),
                ('permissions', models.ManyToManyField(related_name='+', to='ore.repo.Permission')),
                ('project', models.ForeignKey(related_name='teams', to='ore.repo.Project')),
                ('users', models.ManyToManyField(related_name='projectteams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='organizationteam',
            name='permissions',
            field=models.ManyToManyField(related_name='+', to='ore.repo.Permission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationteam',
            name='projects',
            field=models.ManyToManyField(related_name='organizationteams', to='ore.repo.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organizationteam',
            name='users',
            field=models.ManyToManyField(related_name='organizationteams', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
