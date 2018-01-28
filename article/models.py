# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from slugify import slugify


# Create your models here.
class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)
    articles_like = models.CharField(max_length=100,default=timezone.now())

    users_like = models.ManyToManyField(User,related_name="articles_like",blank=True) #字段名

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),) #为每篇文章的id和slug获取文章对象，建立索引后，提高读取速度

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):    #重写save方法，目的实现以下slugify转换方法
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # reverse(viewname,urlconf=None,args=None,kwargs=None,Current_app=None)
        # 参数viewname就是在每个应用的urls.py中设置的URL时的值
        return reverse("article:article_detail", args=[self.id, self.slug])