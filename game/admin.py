from django.contrib import admin

from content.models import ClanModel
from game.models import GameSettingsModel, BonusItemModel


# Register your mode

@admin.register(GameSettingsModel)
class GameSettingsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'description')
    search_fields = ('name',)

@admin.register(BonusItemModel)
class BonusItemModelAdmin(admin.ModelAdmin):
    exclude = ('is_system', )
    list_display = ('title', 'system_name', 'price', 'reward', 'is_system', 'is_shop', 'is_box', 'chance')
    search_fields = ('title',)
