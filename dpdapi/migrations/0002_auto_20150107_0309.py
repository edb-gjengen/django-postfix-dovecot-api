# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpdapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alias',
            options={'verbose_name_plural': 'aliases'},
        ),
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.CharField(unique=True, max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=75),
            preserve_default=True,
        ),
    ]
