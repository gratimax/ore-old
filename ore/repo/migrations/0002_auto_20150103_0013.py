# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repouser',
            old_name='date_created',
            new_name='date_joined',
        ),
    ]
