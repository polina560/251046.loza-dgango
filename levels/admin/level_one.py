from django.contrib import admin

from levels.models import LevelOneDialogue, LevelOne, LevelOneDialogueEnd, LevelOneContainer


class LevelOneDialogueInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image')
    model = LevelOneDialogue

class LevelOneDialogueEndInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image', 'earthquake')
    model = LevelOneDialogueEnd

class LevelOneContainerInline (admin.StackedInline):
    list_display = ('type', 'title', 'text', 'info', 'image')
    model = LevelOneContainer

@admin.register(LevelOne)
class LevelOneAdmin(admin.ModelAdmin):
    extra = 1
    list_display = ('title',)
    inlines = [
        LevelOneDialogueInline,
        LevelOneContainerInline,
        LevelOneDialogueEndInline
    ]