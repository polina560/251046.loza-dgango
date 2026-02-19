from django.contrib import admin

from rating.models import StagesModel, StagePrizesModel, UserRatingModel, ClanRatingModel


# Register your models here.

class StagePrizesModelInline (admin.StackedInline):
    list_display = ('title', 'description')
    model = StagePrizesModel

@admin.register(StagesModel)
class StagesModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_at', 'end_at')

    inlines = [StagePrizesModelInline]

@admin.register(ClanRatingModel)
class ClanRatingModelAdmin(admin.ModelAdmin):
    list_display = ('clan', 'stage', 'total_glory')

@admin.register(UserRatingModel)
class UserRatingModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'clan', 'stage', 'glory', 'glory_time')