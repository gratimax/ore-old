# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+([\\w.@+ -]*[\\w.@+-]+)?$', 'Enter a valid file name.', 'invalid')], verbose_name='name', max_length=32)),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a namespace organization name.', 'invalid')], verbose_name='name', unique=True, max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepoUser',
            fields=[
                ('namespace_ptr', models.OneToOneField(serialize=False, to='ore.repo.Namespace', primary_key=True, auto_created=True, parent_link=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(verbose_name='email', blank=True, max_length=75)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_created', models.DateTimeField(verbose_name='creation date', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='groups', related_query_name='user', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', related_query_name='user', related_name='user_set', help_text='Specific permissions for this user.', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('repo.namespace', models.Model),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('namespace_ptr', models.OneToOneField(serialize=False, to='ore.repo.Namespace', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
            },
            bases=('repo.namespace',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid project name.', 'invalid')], verbose_name='name', max_length=32)),
                ('description', models.TextField(verbose_name='description')),
                ('namespace', models.ForeignKey(related_name='projects', to='ore.repo.Namespace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+([\\w.@+ -]*[\\w.@+-]+)?$', 'Enter a valid version name.', 'invalid')], verbose_name='name', max_length=32)),
                ('description', models.TextField(verbose_name='description')),
                ('project', models.ForeignKey(related_name='versions', to='ore.repo.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='version',
            field=models.ForeignKey(related_name='files', to='ore.repo.Version'),
            preserve_default=True,
        ),
    ]
