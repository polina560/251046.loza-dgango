from django.contrib import admin

from game.models.FAQ import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    exclude = ('position', )
    search_fields = ["question", "answer", "created_at", "updated_at"]
    list_display = ("question", "answer")
