"""spider_server URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url
from main_spider import cj_xm,cj_gz,cj_rw
urlpatterns = [
    url(r'ADD_CJ_XM/', cj_xm.add_cj_xm, name='add_cj_xm'),
    url(r'GET_CJ_XM/', cj_xm.get_cj_xm, name='get_cj_xm'),
    url(r'UPDATE_CJ_XM/', cj_xm.update_cj_xm, name='update_cj_xm'),
    url(r'DELETE_CJ_XM/', cj_xm.delete_cj_xm, name='delete_cj_xm'),

    url(r'ADD_CJ_GZ/', cj_gz.add_cj_gz, name='add_cj_gz'),
    url(r'GET_CJ_GZ/', cj_gz.get_cj_gz, name='get_cj_gz'),
    url(r'GET_CJ_GZ_ID/', cj_gz.get_cj_gz_id, name='get_cj_gz_id'),
    url(r'UPDATE_CJ_GZ/', cj_gz.update_cj_gz, name='update_cj_gz'),
    url(r'DELETE_CJ_GZ/', cj_gz.delete_cj_gz, name='delete_cj_gz'),

    url(r'ADD_CJ_RW/', cj_rw.add_cj_rw, name='add_cj_rw'),
    url(r'GET_CJ_RW/', cj_rw.get_cj_rw, name='get_cj_rw'),
    url(r'UPDATE_CJ_RW/', cj_rw.update_cj_rw, name='update_cj_rw'),
    url(r'DELETE_CJ_RW/', cj_rw.delete_cj_rw, name='delete_cj_rw'),

]
