# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image


# Create your views here.
@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    # 利用提交的数据建立表单类实例
    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            #重写了save()方法
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return JsonResponse({'status': "1"})
        except:
            return JsonResponse({'status': "0"})


@login_required(login_url='/account/login/')
def list_images(request):
    # 获取当前用户的所有图片对象
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/list_images.html', {"images": images})
