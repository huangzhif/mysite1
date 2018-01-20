# -*- coding: utf-8 -*-
from django import forms
from .models import ArticleColumn, ArticlePost


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)  # 用于表单编辑框


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body")
