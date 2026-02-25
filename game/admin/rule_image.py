from ckeditor.widgets import CKEditorWidget
from django.contrib import admin

from game.models.rule_image import RuleImage


@admin.register(RuleImage)
class RuleImageAdmin(admin.ModelAdmin):
    exclude = ('position', )
    search_fields = ["created_at", "updated_at"]
    list_display = ("image", )
