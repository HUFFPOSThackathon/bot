# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fbid', models.CharField(max_length=250)),
                ('location', models.CharField(default=b'NULL', max_length=250)),
                ('state', models.CharField(default=b'NULL', max_length=1000)),
                ('name', models.CharField(default=b'NULL', max_length=1000)),
                ('issue', models.CharField(default=b'NULL', max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
