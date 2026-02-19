from django.contrib import admin

from log.models import UserGames, CouponModel


# Register your models here.

@admin.register(UserGames)
class UserGamesAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'ended_at', 'status')

@admin.register(CouponModel)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'description')