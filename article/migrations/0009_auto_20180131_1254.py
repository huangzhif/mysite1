# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 12:54
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0008_auto_20180130_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='articles_like',
            field=models.CharField(default=datetime.datetime(2018, 1, 31, 12, 54, 39, 233814, tzinfo=utc), max_length=100),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 31, 12, 54, 39, 233763, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='articlepost',
            name='article_tag',
            field=models.ManyToManyField(blank=True, related_name='article_tag', to='article.ArticleTag'),
        ),
    ]
