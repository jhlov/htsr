# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_new_rating(rating_a, rating_b, score):
    k = 30.

    # 예상 스코어
    expected_score = get_expected_score(rating_a, rating_b)
    print 'score : {0}, expected_score : {1}'.format(score, expected_score)

    # 레이팅
    new_rating = rating_a + k * (score - expected_score)
    return new_rating


def get_expected_score(rating_a, rating_b):
    return 1. / (1. + pow(10., (rating_b - rating_a) / 400.))