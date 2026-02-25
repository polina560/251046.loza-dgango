from django.contrib import admin

from game.models.stage import Stage
from game.models.stage_prize import StagePrize


class StagePrizesModelInline (admin.StackedInline):
    list_display = ('title', 'description')
    model = StagePrize

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at')

    inlines = [StagePrizesModelInline]