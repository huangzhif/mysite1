# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required  # 若未登录则跳到登录界面
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import ArticleColumn
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, CommentForm, ArticleTagForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
import redis
from django.conf import settings

# 创建StrictRedis对象，与redis服务器建立链接
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# Create your views here.
@login_required(login_url='/account/login/')
def article_column(request):
    column = ArticleColumn.objects.filter(user=request.user)
    return render(request, "article/column/article_column.html", {"columns": column})


@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, "column_form": column_form})

    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)

        if columns:
            return HttpResponse('2')

        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


# 修改模块函数
@login_required(login_url='/account/login/')
@require_POST  # 保证此视图函数只接收POST方式提交的数据
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


# 删除模块函数
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")

        else:
            return HttpResponse("3")

    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form,
                                                                    "article_columns": article_columns})


@login_required(login_url='/account/login/')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 10)  # 每页10条数据
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page})


@login_required(login_url='/account/login')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # 记录访问次数，以‘article：id:views’为键来记录次数
    total_views = r.incr("article:{}:views".format(article.id))

    # 实现article_ranking中的article.id以步长1 自增，每访问一次，id值增加1
    r.zincrby('article_ranking', article.id, 1)
    # 返回有序集中，指定区间内的成员，成员的位置按分数值递增来排序
    # start：0 ，-1表示最后一个成员,只取10个成员
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]

    article_ranking_ids = [int(id) for id in article_ranking]

    # id__in 功能是查询id在article_ranking_ids中的所有文章对象，并以文章对象为元素生成列表
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))

    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    if request.method == "POST":
        # 直接获取表单提交的内容
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, "article/column/article_detail.html", {"article": article, "total_views": total_views,
                                                                  "most_viewed": most_viewed,
                                                                  "comment_form": comment_form})


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_column = article.column
        return render(request, "article/column/redit_article.html",
                      {"article": article, "article_columns": article_columns,
                       "this_article_column": this_article_column,
                       "this_article_form": this_article_form})

    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


#添加tag视图
@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)  # 获取当前用户下的所有标签
        article_tag_form = ArticleTagForm()  # 实例化一个form表单
        return render(request, 'article/tag/tag_list.html',
                      {"article_tags": article_tags, "article_tag_form": article_tag_form})

    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)  # 获取表单post回来的值
        if tag_post_form.is_valid():#执行验证并返回一个表示数据是否合法的布尔值 如：是否必录
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user #author 为models定义变量
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot be saved.")

        else:
            return HttpResponse("sorry,the form is not valid.")

#删除tag视图
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id) #获取前端回传的tag_id
        tag.delete()            #删除该tag
        return HttpResponse("1")
    except:
        return HttpResponse("2")