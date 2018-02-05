# -*- coding: utf-8 -*-
from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
import urllib
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    #clean_<fieldname>:前端输入数据和后台数据库数据的验证，例如：注册的用户名是否已存在，邮箱是否注册过等；
    def clean_url(self):
        url = self.cleaned_data['url']  # 获取表单返回的url值
        valid_extensions = ['jpg', 'jpeg', 'png']
        # rspit('.',1) 从右边起 以.分割1次，并且把分割开的两边以list保存，[1]: 取列表第二个值
        extension = url.rsplit('.', 1)[1].lower()
        # 如果该后缀没有在valid_extensions 里，则抛出异常
        if extension not in valid_extensions:
            raise forms.ValidationError("The Error Url does not match valid image extension.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        #继承父类的save方法
        image = super(ImageForm, self).save(commit=False)
        #获取表单返回的url方法
        image_url = self.cleaned_data['url']
        #拼成一个图片名
        image_name = '{0}.{1}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        #打开地址
        response = urllib.urlopen(image_url)
        #防止重名，会自动下划线加字符格式保证上传成功
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()

        return image
