# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-10 07:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_auto_20180209_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='articles_like',
            field=models.CharField(default=datetime.datetime(2018, 2, 10, 7, 30, 21, 559206, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 10, 7, 30, 21, 559165, tzinfo=utc)),
        ),
    ]
