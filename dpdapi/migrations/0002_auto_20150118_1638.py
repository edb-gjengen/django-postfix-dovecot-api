# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpdapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='alias',
            unique_together=set([('source', 'destination', 'domain')]),
        ),
    ]
