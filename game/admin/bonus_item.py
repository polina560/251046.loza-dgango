from django.contrib import admin
from game.models.bonus_item import BonusItem


@admin.register(BonusItem)
class BonusItemAdmin(admin.ModelAdmin):
    exclude = ('is_system', )
    list_display = ('title', 'system_name', 'price', 'reward', 'is_system', 'is_shop', 'is_box', 'chance')
    search_fields = ('title',)