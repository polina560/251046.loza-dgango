from django.contrib import admin
from game.models.sale import Sale


@admin.register(Sale)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('title', )