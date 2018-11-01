"""seasonally URL Configuration

"""
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from suggest import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^recipe/', views.recipe),
    url(r'^infographic/', views.infographic),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('api.urls')),
    url(r'^robots\.txt/$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^ads\.txt/$', TemplateView.as_view(
        template_name='ads.txt', content_type='text/plain')),
]
