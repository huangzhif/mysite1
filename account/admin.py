# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import UserProfile, UserInfo


# Register your models here.
# 用于在管理员页面显示字段信息
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')
    list_filter = ("phone",)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "company", "profession", "address", "aboutme", "photo")
    list_filter = ("school", "company", "profession")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
