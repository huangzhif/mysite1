# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-10 07:30
from __future__ import unicode_literals

import course.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video', models.FileField(upload_to=course.models.user_directory_path)),
                ('description', models.TextField(blank=True)),
                ('attach', models.FileField(blank=True, upload_to=course.models.user_directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='course.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
