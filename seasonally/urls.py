"""seasonally URL Configuration

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from suggest import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('api.urls')),
]
