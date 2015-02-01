# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OreUser',
            fields=[
                ('namespace_ptr', models.OneToOneField(auto_created=True, to='ore.core.Namespace', serialize=False, parent_link=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='email')),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='creation date', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, verbose_name='groups', related_query_name='user', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', related_query_name='user', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.namespace', models.Model),
        ),
    ]
