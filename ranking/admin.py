# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Player, DoublesPlayer, Result

admin.site.register(Player)
admin.site.register(DoublesPlayer)
admin.site.register(Result)