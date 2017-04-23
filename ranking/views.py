# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
import os

from .models import Player, DoublesPlayer


# 랭킹 페이지
def ranking(request):

    # 싱글 랭킹
    singles = Player.objects.filter(rating__gt=0).order_by('rating')

    # 더블 랭킹
    doubles = DoublesPlayer.objects.filter(rating__gt=0).order_by('rating')

    data = {
        'singles': singles,
        'doubles': doubles,
    }

    return render(request, 'ranking.html', data)