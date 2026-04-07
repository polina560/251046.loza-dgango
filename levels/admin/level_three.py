from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from levels.models import LevelThreeDialogue, LevelThreeDialogueEnd, LevelThreeDialogueExpl, LevelThreeInfo, \
    LevelThreeResults, LevelThree
from levels.models.level_two import LevelTwoDialogue, LevelTwoDialogueEnd, LevelTwo


class LevelThreeDialogueInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image')
    model = LevelThreeDialogue

class LevelThreeDialogueEndInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image')
    model = LevelThreeDialogueEnd

class LevelThreeDialogueExplInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image')
    model = LevelThreeDialogueExpl

class LevelThreeInfoInline (admin.StackedInline):
    extra = 1
    fields = ('title', 'text')
    model = LevelThreeInfo

class LevelThreeResultsInline (admin.StackedInline):
    extra = 1
    fields = ('title', 'description', 'image', 'process_video', 'result_video')
    model = LevelThreeResults


@admin.register(LevelThree)
class LevelThreeAdmin(admin.ModelAdmin):
    extra = 1
    inlines = [
        LevelThreeDialogueInline,
        LevelThreeDialogueExplInline,
        LevelThreeInfoInline,
        LevelThreeResultsInline,
        LevelThreeDialogueEndInline,
    ]

    def changelist_view(self, request, extra_context=None):
        """Переопределяем список записей"""
        obj = LevelThree.objects.first()

        if obj is not None:
            url = reverse('admin:levels_levelthree_change', args=[obj.id])
            return HttpResponseRedirect(url)
        else:
            url = reverse('admin:levels_levelthree_add')
            return HttpResponseRedirect(url)

    def has_add_permission(self, request):
        """Запрещаем создание новой записи, если уже есть одна"""
        if LevelThree.objects.exists():
            return False
        return super().has_add_permission(request)