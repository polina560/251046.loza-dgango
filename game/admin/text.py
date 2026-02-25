from django.contrib import admin

from game.models.text import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    search_fields = ["key", "created_at", "updated_at"]
    # list_filter = "key"
    list_display = ("key", "text", "created_at")
    # list_editable = ("key", "text")
    # list_display_links = ("key",)

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # Применяем CKEditor только к полю 'text'
    #     form.base_fields['text'].widget = CKEditorWidget()
    #     return form
