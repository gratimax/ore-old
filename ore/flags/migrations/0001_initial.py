# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(
                    serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', model_utils.fields.StatusField(choices=[('new', 'new'), ('quashed', 'quashed'), ('retracted', 'retracted'), (
                    'content_removed_moderator', 'content_removed_moderator'), ('content_removed_creator', 'content_removed_creator')], max_length=100, no_check_for_status=True, default='new')),
                ('date_flagged', models.DateTimeField(auto_now_add=True)),
                ('date_resolved', models.DateTimeField(
                    null=True, blank=True, default=None)),
                ('flag_type', model_utils.fields.StatusField(choices=[('inappropriate', 'inappropriate'), (
                    'spam', 'spam')], max_length=100, no_check_for_status=True, default='inappropriate')),
                ('extra_comments', models.TextField(blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(
                    to='contenttypes.ContentType')),
                ('flagger', models.ForeignKey(
                    related_name='flagger_flags', to=settings.AUTH_USER_MODEL)),
                ('resolver', models.ForeignKey(null=True, blank=True,
                                               to=settings.AUTH_USER_MODEL, related_name='resolver_flags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
