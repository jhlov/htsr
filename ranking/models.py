# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# 플레이어
class Player(models.Model):
    name = models.CharField('이름', max_length=30, db_index=True)
    win = models.IntegerField('승', default=0)
    lose = models.IntegerField('패', default=0)
    rating = models.IntegerField('레이팅', default=0, db_index=True)

    def __unicode__(self):
        return self.name


# 복식 랭킹을 위한 모델
class DoublesPlayer(models.Model):
    player_1 = models.ForeignKey('Player', related_name='player_1')
    player_2 = models.ForeignKey('Player', related_name='player_2')
    win = models.IntegerField('승', default=0)
    lose = models.IntegerField('패', default=0)
    rating = models.IntegerField('레이팅', default=0, db_index=True)

    def __unicode__(self):
        return '{0} {1}'.format(self.player_1, self.player_2)


# 경기 결과
class Result(models.Model):
    regist_date = models.DateTimeField('등록 시간', auto_now=True)
    play_date = models.DateTimeField('경기 시간', db_index=True)
    blue_player = models.IntegerField('블루 플레이어 id', db_index=True)
    red_player = models.IntegerField('레드 플레이어 id', db_index=True)
    blue_score = models.IntegerField('블루 점수')
    red_score = models.IntegerField('레드 점수')
    is_single = models.BooleanField('싱글플레이 여부', db_index=True)
    blue_rating_delta = models.IntegerField('블루 점수 변동')
    red_rating_delta = models.IntegerField('레드 점수 변동')