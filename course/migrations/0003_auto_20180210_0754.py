# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-10 07:54
from __future__ import unicode_literals

import course.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_lesson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='lesson',
            name='order',
            field=course.fields.OrderField(blank=True, null=True),
        ),
    ]