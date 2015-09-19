# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intField', models.IntegerField(default=2)),
                ('charField', models.CharField(default=b'a', max_length=1)),
                ('textField', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
