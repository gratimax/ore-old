# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0009_auto_20150103_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='version',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set([('version', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationteam',
            unique_together=set([('organization', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('namespace', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectteam',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('project', 'name')]),
        ),
    ]
