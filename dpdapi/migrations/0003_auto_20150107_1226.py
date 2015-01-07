# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpdapi', '0002_auto_20150107_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alias',
            name='destination',
            field=models.EmailField(max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alias',
            name='source',
            field=models.EmailField(max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
            preserve_default=True,
        ),
    ]
