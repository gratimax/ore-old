# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_merge'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='page',
            order_with_respect_to='parent',
        ),
    ]
