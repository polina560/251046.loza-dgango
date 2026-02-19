from django.contrib import admin

from log.models import UserGames


# Register your models here.

@admin.register(UserGames)
class UserGamesInline(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'ended_at', 'status')