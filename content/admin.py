from ckeditor.widgets import CKEditorWidget
from django.contrib import admin

from content.models import TextModel, ClanModel, FAQModel, RuleImageModel


# Register your models here.
@admin.register(RuleImageModel)
class RuleImageModel(admin.ModelAdmin):
    exclude = ('position', )
    search_fields = ["created_at", "updated_at"]
    list_display = ("image", )

@admin.register(FAQModel)
class FAQModelAdmin(admin.ModelAdmin):
    exclude = ('position', )
    search_fields = ["question", "answer", "created_at", "updated_at"]
    list_display = ("question", "answer")

@admin.register(ClanModel)
class ClanModelAdmin(admin.ModelAdmin):
    search_fields = ["title", "system_name", "created_at", "updated_at"]
    list_display = ("title", "system_name", "image")

@admin.register(TextModel)
class TextModelAdmin(admin.ModelAdmin):
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


