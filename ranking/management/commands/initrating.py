# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db import transaction
from ranking.models import Player, DoublesPlayer, Result

import ranking.utils


class Command(BaseCommand):
    args = '<no_arguments ...>'
    help = 'Init Database for new environment'

    @transaction.atomic
    def handle(self, *args, **options):

        # 모든 선수들의 레이팅을 초기화
        Player.objects.update(rating=1000)

        # 결과를 플레이 시간 역순으으로 불러 온다
        singles_results = Result.objects.filter(is_single=True).order_by('play_date')
        for result in singles_results:
            player_a = Player.objects.get(id=result.blue_player)
            player_b = Player.objects.get(id=result.red_player)

            self.post_process(result, player_a, player_b)

        doubles_results = Result.objects.filter(is_single=False).order_by('play_date')
        for result in doubles_results:
            player_a = DoublesPlayer.objects.get(id=result.blue_player)
            player_b = DoublesPlayer.objects.get(id=result.red_player)

            self.post_process(result, player_a, player_b)


    def post_process(self, result, player_a, player_b):
        print '{0} {1} : {2} {3}'.format(
            player_a.name, result.blue_score, result.red_score, player_b.name)

        player_a_old_rating = player_a.rating
        player_b_old_rating = player_b.rating

        score_a = result.blue_score
        score_b = result.red_score

        new_rating_a = \
            ranking.utils.get_new_rating(
                player_a_old_rating,
                player_b_old_rating,
                float(score_a) / float(score_a + score_b)
            )

        print '{0} {1} -> {2}'.format(
            player_a.name, player_a_old_rating, new_rating_a)

        new_rating_b = \
            ranking.utils.get_new_rating(
                player_b_old_rating,
                player_a_old_rating,
                float(score_b) / float(score_a + score_b)
            )

        print '{0} {1} -> {2}'.format(
            player_b.name, player_b_old_rating, new_rating_b)

        print '=========================================================='

        result.blue_rating_old = player_a_old_rating
        result.red_rating_old = player_b_old_rating
        result.blue_rating_delta = new_rating_a - player_a_old_rating
        result.red_rating_delta = new_rating_b - player_b_old_rating
        result.save()

        player_a.rating = new_rating_a
        player_a.save()

        player_b.rating = new_rating_b
        player_b.save()


