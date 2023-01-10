"""seasonally API URL Configuration

"""
from django.urls import re_path

from api import views


urlpatterns = [
    re_path(r'^add-recipe/$', views.add_recipe),
    re_path(r'^add-product/$', views.add_product),
    re_path(r'^add-month/$', views.add_month),
    re_path(r'^recipe/$', views.recipe),
    re_path(r'^product/$', views.product),
]
