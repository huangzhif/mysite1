# -*- coding:utf-8 -*-

# template库，包含着诸多与模板有关的类和方法
from django import template

# register对象包含了simple_tag及其他方法，将用于自定义标签
register = template.Library()

from article.models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    # 返回以下变量到装饰器中的模板，模板获取参数显示在页面
    return {"latest_articles":latest_articles}