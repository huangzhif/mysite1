# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login  # django内置用户认证方法
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect


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
                return HttpResponse("password is not right")
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
            new_profile.user = new_user
            new_profile.save()

            UserInfo.objects.create(user=new_user)  # 保护用户注册信息后，同时在account_userinfo 数据库表中写入该用户的ID信息

            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry,you can not register.")

    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})


# 因为只有登录的用户才能看到自己的个人信息，所以要在该视图函数被执行时判断用户是否登录，此处使用了Django自带的装饰器函数，所以在前面
# 引入了装饰器函数login_required。在具体使用时，向装饰器函数提供一个参数，将未登录的用户转到登录界面
@login_required(login_url='/account/login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user": user, "userinfo": userinfo, "userprofile": userprofile})


@login_required(login_url='/account/login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data

            print user_cd["email"]
            user.email = user_cd["email"]
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()

        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})

        userinfo_form = UserInfoForm(
            initial={"school": userinfo.school, "company": userinfo.company, "profession": userinfo.profession,
                     "address": userinfo.address, "aboutme": userinfo.aboutme})

        return render(request, "account/myself_edit.html",
                      {"user_form": user_form, "userprofile_form": userprofile_form, "userinfo_form": userinfo_form})


def my_image(request):
    return render(request, 'account/imagecrop.html', )

@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo=img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',)
