from django.contrib import admin

from game.models.clan import Clan


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    search_fields = ["title", "system_name", "created_at", "updated_at"]
    list_display = ("title", "system_name", "image")
