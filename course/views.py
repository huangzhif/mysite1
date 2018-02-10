# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import CreateView, DeleteView
from .models import Course, Lesson
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from .forms import CreateCourseForm, CreateLessonForm

from django.http import HttpResponse
from django.views import View
import json


# Create your views here.

class CourseListView(ListView):
    # 方法：
    # get_queryset——–或者需要展示的数据并且返回（必须要有返回）
    # get_context_data——–传递额外的数据到模板（html）。

    # 变量：
    # paginate_by 如果做分页这个参数说明每页有几个item项
    # http_mothod_names 请求类型 可以是get或者post
    model = Course  # 对应的模型（Model）
    # queryset = Course.objects.filter(user=User.objects.filter(username="admin"))
    context_object_name = "courses"  # 在模板中的变量名 {{name}}
    template_name = 'course/course_list.html'  # {{模板一般是一个html文件名}}


class UserMixin(MultipleObjectMixin):
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


# CreateView:一个通用视图类，当用户以GET方式请求时，即在页面中显示表单
class CreateCourseView(UserCourseMixin, CreateView):
    object_list = ''
    # model = Course
    # login_url = "/account/login/"
    fields = ['title', 'overview']
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form": form})


class DeleteCourseView(UserCourseMixin, DeleteView):
    object_list = ''
    # template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "OK"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


class CreateLessonView(LoginRequiredMixin, View):
    model = Lesson
    login_url = "/account/login/"

    def get(self, request, *args, **kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request, "course/manage/create_lesson.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateLessonForm(self.request.user, request.POST, request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonsView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return self.render_to_response({'course': course})

    def post(self,request,*args,**kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.student.add(self.request.user)
        return HttpResponse("ok")

class DetailLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get(self,request,lesson_id):
        lesson = get_object_or_404(Lesson,id=lesson_id)
        return self.render_to_response({"lesson":lesson})


class StudentListLessonView(ListLessonsView):
    template_name = "course/slist_lessons.html"

