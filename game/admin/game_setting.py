from django.contrib import admin

from game.models.game_setting import GameSetting


@admin.register(GameSetting)
class GameSettingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'description')
    search_fields = ('name',)