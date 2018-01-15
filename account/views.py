# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login  # django内置用户认证方法
from .forms import LoginForm, RegistrationForm, UserProfileForm

from django.shortcuts import render


# Create your views here.
def user_login(request):
    if request.method == "POST":  # 登录用户密码认证
        login_form = LoginForm(request.POST)  # 获取到用户名密码
        if login_form.is_valid():  # 判断前端提交到后端的数据是否符合表单类属性要求
            # cleaned_data是实例的属性，它以字典形式返回实例的具体数据，即经过检验之后的属性及其值。
            # 如果传入的某项数据不合法，则在cleaned_data的结果中不予显示
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return HttpResponse("Welcome you.you have been authenticated successfully")
            else:
                return HttpResponse("Invalid login")

    if request.method == "GET":  # 打开网站
        login_form = LoginForm()  # 第一次访问网站，获取未绑定数据的表单实例
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user= new_user
            new_profile.save()
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry,you can not register.")

    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})
