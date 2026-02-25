from django.contrib import admin

from game.models.clan_rating import ClanRating


@admin.register(ClanRating)
class ClanRatingAdmin(admin.ModelAdmin):
    list_display = ('clan', 'stage', 'total_glory')