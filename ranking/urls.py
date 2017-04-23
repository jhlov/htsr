# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView
import views


urlpatterns = [
    url(r'^$', views.ranking, name='ranking'),
]
