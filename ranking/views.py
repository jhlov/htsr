# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
import os
from math import pow


from .models import Player, DoublesPlayer, Result


# 랭킹 페이지
def ranking(request):

    # 싱글 랭킹
    singles = Player.objects.filter(Q(win__gt=0) | Q(lose__gt=0)).order_by('-rating')

    # 더블 랭킹
    doubles = DoublesPlayer.objects.all().order_by('rating')

    data = {
        'singles': singles,
        'doubles': doubles,
    }

    return render(request, 'ranking.html', data)


# 점수 등록 페이지
def regist(request):

    players = Player.objects.all()
    return render(request, 'regist.html', {'players': players, 'range': range(11)})



# 싱글 기록 등록
def regist_single(request):

    if request.method == 'POST':
        post = request.POST.copy()

        # 에러체크
        # 선수 이름이 달라야 함
        if post['blue_player'] == post['red_player']:
            return HttpResponse("error : 선수가 동일합니다.")

        # 한쪽이 10점이 되어야 함
        blue_score = int(post['blue_score'])
        red_score = int(post['red_score'])
        if blue_score < 10 and red_score < 10:
            return HttpResponse("error : 점수가 잘 못 되었습니다.")

        if blue_score == 10 and red_score == 10:
            return HttpResponse("error : 점수가 잘 못 되었습니다. (1)")

        blue_player = Player.objects.get(id=int(post['blue_player']))
        red_player = Player.objects.get(id=int(post['red_player']))

        blue_new_rating = get_new_rating(blue_player, red_player, blue_score > red_score)
        print blue_new_rating
        red_new_rating = get_new_rating(red_player, blue_player, red_score > blue_score)
        print red_new_rating

        # 경기 기록
        r = Result.objects.create(
            blue_player=blue_player.id,
            red_player=red_player.id,
            blue_score=blue_score,
            red_score=red_score,
            is_single=True,
            blue_rating_delta=(blue_new_rating - blue_player.rating),
            red_rating_delta=(red_new_rating - red_player.rating))

        r.save()

        # 레이팅 갱신
        blue_player.rating = blue_new_rating
        if blue_score > red_score:
            blue_player.win = blue_player.win + 1
        else:
            blue_player.lose = blue_player.lose + 1
        blue_player.save()

        red_player.rating = red_new_rating
        if blue_score < red_score:
            red_player.win = red_player.win + 1
        else:
            red_player.lose = red_player.lose + 1
        red_player.save()

        return HttpResponse("success")

    return HttpResponse("error")


# 새로운 레이팅 계산
# player_a_score : a가 이겼을 때 1, 졌으면 0
def get_new_rating(player_a, player_b, player_a_score):

    # 예상 승수
    expect_score = get_expect_score(player_a, player_b)

    # 레이팅
    new_rating = player_a.rating + 16 * (player_a_score - expect_score)

    return new_rating


# 예상 승수
def get_expect_score(player_a, player_b):
    return 1 / (1 + pow(10, (player_b.rating - player_a.rating) / 400))
