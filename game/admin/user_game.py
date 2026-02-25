from django.contrib import admin

from game.models.user_game import UserGames


# Register your models here.

@admin.register(UserGames)
class UserGamesAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'ended_at', 'status')
