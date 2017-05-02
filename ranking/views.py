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
from datetime import datetime


from .models import Player, DoublesPlayer, Result
import utils


# 랭킹 페이지
def ranking(request):

    # 싱글 랭킹
    singles = Player.objects.filter(Q(win__gt=0) | Q(lose__gt=0)).order_by('-rating')

    # 더블 랭킹
    doubles = DoublesPlayer.objects.all().order_by('-rating')

    data = {
        'singles': singles,
        'doubles': doubles,
    }

    return render(request, 'ranking.html', data)


# 점수 등록 페이지
def regist(request):

    players = Player.objects.order_by('-win')
    return render(request, 'regist.html', {'players': players, 'range': range(11)})



# 싱글 기록 등록
def regist_single(request):

    if request.method == 'POST':
        post = request.POST.copy()

        # 에러체크
        # 선수 이름이 달라야 함
        if post['blue_player'] == post['red_player']:
            return HttpResponse("error : 선수가 동일합니다.")

        blue_score = int(post['blue_score'])
        red_score = int(post['red_score'])
        error_string = is_valid_score(blue_score, red_score)
        if error_string != "":
            return HttpResponse(error_string)

        blue_player = Player.objects.get(id=int(post['blue_player']))
        red_player = Player.objects.get(id=int(post['red_player']))

        regist_post(blue_player, red_player, blue_score, red_score, True)

        return HttpResponse("success")

    return HttpResponse("error")


# 경기 기록 후 처리
def regist_post(blue_player, red_player, blue_score, red_score, is_single):
    blue_new_rating =\
        utils.get_new_rating(
            blue_player.rating,
            red_player.rating,
            float(blue_score) / float(blue_score + red_score))
    red_new_rating =\
        utils.get_new_rating(
            red_player.rating,
            blue_player.rating,
            float(red_score) / float(blue_score + red_score))

    # 경기 기록
    r = Result.objects.create(
        play_date=datetime.now(),
        blue_player=blue_player.id,
        red_player=red_player.id,
        blue_score=blue_score,
        red_score=red_score,
        is_single=is_single,
        blue_rating_old=blue_player.rating,
        red_rating_old=red_player.rating,
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


def is_valid_score(blue_score, red_score):
    # 한쪽이 10점이 되어야 함
    if blue_score < 10 and red_score < 10:
        return "error : 점수가 잘 못 되었습니다."

    if blue_score == 10 and red_score == 10:
        return "error : 점수가 잘 못 되었습니다."

    return ""


# 더블 기록 등록
def regist_double(request):

    if request.method == 'POST':
        post = request.POST.copy()

        # 에러체크
        # 선수 이름이 달라야 함
        if post['blue_player_1'] == post['blue_player_2'] or \
            post['blue_player_1'] == post['red_player_1'] or \
            post['blue_player_1'] == post['red_player_2'] or \
            post['blue_player_2'] == post['red_player_1'] or \
            post['blue_player_2'] == post['red_player_2'] or \
            post['red_player_1'] == post['red_player_2']:
            return HttpResponse("error : 선수가 동일합니다.")


        # 한쪽이 10점이 되어야 함
        blue_score = int(post['blue_score'])
        red_score = int(post['red_score'])
        error_string = is_valid_score(blue_score, red_score)
        if error_string != "":
            return HttpResponse(error_string)

        blue_player = get_double_player(int(post['blue_player_1']), int(post['blue_player_2']))
        red_player = get_double_player(int(post['red_player_1']), int(post['red_player_2']))

        regist_post(blue_player, red_player, blue_score, red_score, False)

        return HttpResponse("success")

    return HttpResponse("error")


def get_double_player(player_1, player_2):
    id_1 = min(player_1, player_2)
    id_2 = max(player_1, player_2)
    player = DoublesPlayer.objects.get_or_create(player_1=id_1, player_2=id_2)
    return player[0]


# 결과 페이지
def result(request):

    # 싱글
    singles = Result.objects.filter(is_single=True).order_by('-play_date')

    # 더블
    doubles = Result.objects.filter(is_single=False).order_by('-play_date')

    data = {
        'singles': singles,
        'doubles': doubles,
    }

    return render(request, 'result.html', data)


def video(request):
    return render(request, 'video.html')