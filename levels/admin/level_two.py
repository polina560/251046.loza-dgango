from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from levels.models.level_two import LevelTwoDialogue, LevelTwoDialogueEnd, LevelTwo


class LevelTwoDialogueInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image')
    model = LevelTwoDialogue

class LevelTwoDialogueEndInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image', 'indicator')
    model = LevelTwoDialogueEnd


@admin.register(LevelTwo)
class LevelTwoAdmin(admin.ModelAdmin):
    extra = 1
    inlines = [
        LevelTwoDialogueInline,
        LevelTwoDialogueEndInline
    ]

    def changelist_view(self, request, extra_context=None):
        """Переопределяем список записей"""
        obj = LevelTwo.objects.first()

        if obj is not None:
            url = reverse('admin:levels_leveltwo_change', args=[obj.id])
            return HttpResponseRedirect(url)
        else:
            url = reverse('admin:levels_leveltwo_add')
            return HttpResponseRedirect(url)

    def has_add_permission(self, request):
        """Запрещаем создание новой записи, если уже есть одна"""
        if LevelTwo.objects.exists():
            return False
        return super().has_add_permission(request)