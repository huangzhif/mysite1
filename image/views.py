# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    # 利用提交的数据建立表单类实例
    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            # 重写了save()方法
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return JsonResponse({'status': "1"})
        except:
            return JsonResponse({'status': "0"})


@login_required(login_url='/account/login/')
def list_images(request):
    # 获取当前用户的所有图片对象
    images_list = Image.objects.filter(user=request.user)
    paginator = Paginator(images_list, 3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        images = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        images = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        images = current_page.object_list
    return render(request, 'image/list_images.html', {"images": images, "page": current_page})


# 删除图片
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_image(request):
    image_id = request.POST['image_id']
    try:
        # 获取该ID 对象
        image = Image.objects.get(id=image_id)
        image.delete()
        return JsonResponse({'status': "1"})
    except:
        return JsonResponse({'status': "1"})


def falls_images(request):
    # 获取所有图片
    # images = Image.objects.all()
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/falls_images.html', {"images": images})
