from django.contrib import admin

from game.models.coupon import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'description')
