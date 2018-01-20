# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import ArticleColumn
from django.contrib import admin


# Register your models here.
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user') #字段
    list_filter = ("column",) #过滤条件
    search_fields = ('column',) #查询条件
    # 添加这个选项之后，修改列表上边会显示一个日期层级导航栏，这个导航栏先显示年份，然后向下显示月份和具体某一天。
    date_hierarchy = 'created'
    ordering = ('-created',) #排序


admin.site.register(ArticleColumn, ArticleColumnAdmin)
