from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'about/$', TemplateView.as_view(template_name="course/about.html"),name='about'),
]