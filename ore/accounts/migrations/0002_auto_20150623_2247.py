# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ore.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='oreuser',
            managers=[
                ('objects', ore.accounts.models.OreUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='oreuser',
            name='email',
            field=models.EmailField(
                verbose_name='email', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='oreuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                         related_query_name='user', related_name='user_set', verbose_name='groups', to='auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='oreuser',
            name='last_login',
            field=models.DateTimeField(
                verbose_name='last login', null=True, blank=True),
        ),
    ]
