# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
"""mysite1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
     url()

http://blog.csdn.net/hackerain/article/details/40701099

先来看下最重要的url()方法。
第一个参数regex是代表URL的正则表达式，第二个参数指定了和该正则表达式映射的View，
此外，还可以通过kwargs参数，给view方法指定默认的kwargs参数，
还有name参数，用来命名该URL，主要用在URL反解中，至于prefix用处不大，不解释。

上面说过，include()是“树”结构关系的联系者，include会关联其他的URLconf到本URLconf，
靠include()才能够让Django的URL设计变得非常的灵活和简洁。include()有三个参数，
第一个参数不必多说，它指定了要包含的其它URLconf的路径，关键是剩下的两个参数，一个是namespace, 一个是app_name，
有什么用呢？其实，这两个参数再加上url()方法中的name参数，共同构成了Django中URL的命名空间，
而命名空间主要是为了URL反解的，那什么是URL反解呢？我们现在能根据请求的一个URL路径，
找到对应的view处理方法，那么反过来，我们在view方法中，或者是template中，根据传递过来的参数，
能够解析出对应的URL，这就是URL反解。为什么需要URL反解呢？主要是为了不要把程序写死了，
如果我们在html中直接把路径写死了，那么以后改起来就会非常的麻烦，所以常常会把这些可变的东西放到一个变量中，
在程序中引用的是这个变量名，这是写程序的一个常识吧。所以，我们能从这个“树”中，从上到下，也得能够从下到上。
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
    url(r'^article/', include('article.urls', namespace='article', app_name="article")),
    url(r'home/', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^image/', include('image.urls', namespace='image', app_name='image'))
]
