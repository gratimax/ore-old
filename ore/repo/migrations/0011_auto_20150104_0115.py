# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('repo', '0010_auto_20150103_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(choices=[('new', 'new'), ('quashed', 'quashed'), ('retracted', 'retracted'), ('content_removed_moderator', 'content_removed_moderator'), ('content_removed_creator', 'content_removed_creator')], no_check_for_status=True, max_length=100, default='new')),
                ('date_flagged', models.DateTimeField(auto_now_add=True)),
                ('date_resolved', models.DateTimeField(null=True, blank=True, default=None)),
                ('flag_type', model_utils.fields.StatusField(choices=[('inappropriate', 'inappropriate'), ('spam', 'spam')], no_check_for_status=True, max_length=100, default='inappropriate')),
                ('extra_comments', models.TextField(blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('flagger', models.ForeignKey(related_name='flagger_flags', to=settings.AUTH_USER_MODEL)),
                ('resolver', models.ForeignKey(related_name='resolver_flags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='flag',
            unique_together=set([('flagger', 'flag_type', 'content_type', 'object_id')]),
        ),
        migrations.AddField(
            model_name='file',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], no_check_for_status=True, max_length=100, default='active'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='namespace',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], no_check_for_status=True, max_length=100, default='active'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], no_check_for_status=True, max_length=100, default='active'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='version',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], no_check_for_status=True, max_length=100, default='active'),
            preserve_default=True,
        ),
    ]
