"""faceRecog URL Configuration

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
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from faceRecog import views as app_views
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^$', app_views.index),
    # url(r'^detect$', app_views.detect),
    url(r'^my_eyes$', app_views.my_eyes),
    path('download_file', app_views.download_file, name='download_file'),
    url(r'^leave$', app_views.leave),
    url(r'^presentation$', app_views.presentation),
    #url(r'^copy_my_eyes$', app_views.copy_my_eyes),
    url(r'^copy_my_eyes/', TemplateView.as_view(template_name="maps.html"),name='copy_my_eyes'),
]
