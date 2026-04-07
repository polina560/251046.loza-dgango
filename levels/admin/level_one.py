from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

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

    def changelist_view(self, request, extra_context=None):
        """Переопределяем список записей"""
        # Проверяем, есть ли уже запись в модели
        obj = LevelOne.objects.first()

        if obj is not None:
            # Если запись существует - перенаправляем на форму редактирования
            url = reverse('admin:levels_levelone_change', args=[obj.id])
            return HttpResponseRedirect(url)
        else:
            # Если записей нет - перенаправляем на форму создания
            url = reverse('admin:levels_levelone_add')
            return HttpResponseRedirect(url)

    def has_add_permission(self, request):
        """Запрещаем создание новой записи, если уже есть одна"""
        if LevelOne.objects.exists():
            return False
        return super().has_add_permission(request)