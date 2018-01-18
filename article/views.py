# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required  # 若未登录则跳到登录界面
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import ArticleColumn
from django.shortcuts import render


# Create your views here.
@login_required(login_url='/account/login/')
def article_column(request):
    column = ArticleColumn.objects.filter(user=request.user)
    return render(request, "article/column/article_column.html", {"columns": column})

