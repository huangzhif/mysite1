# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticlePost, ArticleColumn
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse


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


@csrf_exempt  # 取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id) #获取当前文章的对象
            if action == 'like':
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")
