# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticlePost, ArticleColumn
from django.contrib.auth.models import User


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        article_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all()  # 获取所有文章信息

    paginator = Paginator(article_title, 10)  # 实例化一个分页对象，每页10行
    page = request.GET.get('page')  # 获取页码
    try:
        current_page = paginator.page(page)  # 获取某页对应的记录
        articles = current_page.object_list
    except PageNotAnInteger:  # 如果页码不是一个整数
        current_page = paginator.page(1)  # 取第一页的记录
        articles = current_page.object_list
    except EmptyPage:  # 如果页码太大，没有相应的记录
        current_page = paginator.page(paginator.num_pages)  # 取最后一页记录
        articles = current_page.object_list

    if username:
        return render(request, "article/list/author_articles.html", {"articles": articles, "page": current_page,
                                                                     "userinfo": userinfo, "user": user})

    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})
