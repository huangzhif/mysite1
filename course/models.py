# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User, related_name="courses_user")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)  # 保存slug链接
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    # 重写models的保存方法，同时把经过slug转换的title 保存到slug字段中
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
