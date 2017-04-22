# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# 플레이어
class Player(models.Model):
    name = models.CharField("이름", null=False, max_length=30, db_index=True)
    win = models.IntegerField("승", default=0)
    lose = models.IntegerField("패", default=0)
    rating = models.IntegerField("레이팅", default=0)


# 경기 결과
class Result(models.Model):
    regist_date = models.DateTimeField("등록 시간", auto_now=True)
    play_date = models.DateTimeField("경기 시간", db_index=True)
    blue_player = models.CharField("블루 플레이어 id", max_length=20, db_index=True)
    red_player = models.CharField("레드 플레이어 id", max_length=20, db_index=True)
    blue_score = models.IntegerField("블루 점수")
    red_score = models.IntegerField("레드 점수")
    is_single = models.BooleanField("싱글플레이 여부", db_index=True)
    blue_rating_delta = models.IntegerField("블루 점수 변동")
    red_rating_delta = models.IntegerField("레드 점수 변동")


