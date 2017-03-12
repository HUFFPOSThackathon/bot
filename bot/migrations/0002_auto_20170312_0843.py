# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='location',
            new_name='location_lat',
        ),
        migrations.AddField(
            model_name='person',
            name='location_long',
            field=models.CharField(default=b'NULL', max_length=250),
            preserve_default=True,
        ),
    ]
