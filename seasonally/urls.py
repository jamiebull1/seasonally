"""seasonally URL Configuration

"""
from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin
from django.views.generic import TemplateView

from suggest import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^index/$', views.index),
    re_path(r'^recipe/(?P<slug>[\w-]+)/$', views.recipe),
    re_path(r'^recipe/', views.recipe),
    re_path(r'^infographic/', views.infographic),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/v1/', include('api.urls')),
    re_path(r'^robots\.txt/$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    re_path(r'^ads\.txt/$', TemplateView.as_view(
        template_name='ads.txt', content_type='text/plain')),
]
