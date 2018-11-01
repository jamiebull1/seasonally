"""seasonally API URL Configuration

"""
from django.conf.urls import url

from api import views


urlpatterns = [
    url(r'^add-recipe/$', views.add_recipe),
    url(r'^add-product/$', views.add_product),
    url(r'^add-month/$', views.add_month),
    url(r'^recipe/$', views.recipe),
    url(r'^product/$', views.product),
]
