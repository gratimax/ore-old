# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0017_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='flag',
            unique_together=set([]),
        ),
    ]
