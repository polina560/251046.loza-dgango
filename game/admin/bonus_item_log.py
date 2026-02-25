from django.contrib import admin

from game.models.bonus_item_log import BonusItemLog


@admin.register(BonusItemLog)
class BonusItemLogAdmin(admin.ModelAdmin):
    exclude = ('is_system', 'is_reserve')
