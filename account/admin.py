# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import UserProfile


# Register your models here.
# 用于在管理员页面显示字段信息
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')
    list_filter = ("phone",)


admin.site.register(UserProfile, UserProfileAdmin)
