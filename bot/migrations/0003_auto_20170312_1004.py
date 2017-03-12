# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20170312_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('constituencyName', models.CharField(default=b'NULL', max_length=250)),
                ('problemHits', models.CharField(default=b'NULL', max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem', models.CharField(default=b'NULL', max_length=250)),
                ('problemTag1', models.CharField(default=b'NULL', max_length=250)),
                ('problemTag2', models.CharField(default=b'NULL', max_length=250)),
                ('constituencyName', models.ForeignKey(to='bot.constituency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='mla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('candidateName', models.CharField(default=b'NULL', max_length=250)),
                ('contactDetails', models.CharField(default=b'NULL', max_length=250)),
                ('crimalCases', models.CharField(default=b'NULL', max_length=250)),
                ('educationalQualifications', models.CharField(default=b'NULL', max_length=250)),
                ('constituencyName', models.ForeignKey(to='bot.constituency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='location',
            field=models.CharField(default=b'NULL', max_length=1000),
            preserve_default=True,
        ),
    ]
