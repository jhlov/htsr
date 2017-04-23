# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView
import views


urlpatterns = [
    url(r'^$', views.ranking, name='index'),
    url(r'^ranking', views.ranking, name='ranking'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^regist/single', views.regist_single, name='regist_single'),
    url(r'^result', views.result, name='result'),
]
