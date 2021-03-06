# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from slugify import slugify
from .fields import OrderField


# Create your models here.
class Course(models.Model):
    user = models.ForeignKey(User, related_name="courses_user")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)  # 保存slug链接
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    student = models.ManyToManyField(User,related_name="courses_joined",blank=True)

    class Meta:
        ordering = ('-created',)

    # 重写models的保存方法，同时把经过slug转换的title 保存到slug字段中
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


def user_directory_path(instance, filename):
    return "courses/user_{0}/{1}".format(instance.user.id, filename)


class Lesson(models.Model):
    user = models.ForeignKey(User, related_name='lesson_user')
    course = models.ForeignKey(Course, related_name='lesson')
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=user_directory_path)
    description = models.TextField(blank=True)
    attach = models.FileField(blank=True, upload_to=user_directory_path)
    order = OrderField(blank=True, for_fields=['course'],null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}.{}'.format(self.order, self.title)
