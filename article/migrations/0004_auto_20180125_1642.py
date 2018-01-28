# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-25 16:42
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0003_auto_20180125_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='articlePost_Users_Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_like', models.ManyToManyField(blank=True, related_name='articles_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='articles_like',
            field=models.CharField(default=datetime.datetime(2018, 1, 25, 16, 42, 16, 634600, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 25, 16, 42, 16, 634559, tzinfo=utc)),
        ),
    ]