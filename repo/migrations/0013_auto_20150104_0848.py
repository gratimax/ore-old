# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0012_auto_20150104_0522'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+([\\w.@+ -]*[\\w.@+-]+)?$', 'Enter a valid file type name.', 'invalid')], max_length=32, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('project', models.ForeignKey(related_name='filetypes', to='repo.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='filetype',
            field=models.ForeignKey(default=None, related_name='files', to='repo.FileType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='default_filetype',
            field=models.OneToOneField(default=None, related_name='+', to='repo.FileType'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set([('version', 'filetype')]),
        ),
    ]
