# -*- coding: utf-8 -*-
from django import forms
from .models import ArticleColumn, ArticlePost, Comment,ArticleTag


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)  # 用于表单编辑框


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title", "body")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator", "body",)

#标签新增表单
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ("tag",)