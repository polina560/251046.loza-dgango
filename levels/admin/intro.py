from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from levels.models.intro import IntroDialogue, Intro


class IntroDialogueInline (admin.StackedInline):
    extra = 1
    fields = ('text', 'image')
    model = IntroDialogue

@admin.register(Intro)
class IntroAdmin(admin.ModelAdmin):
    extra = 1
    inlines = [
        IntroDialogueInline,
    ]

    def changelist_view(self, request, extra_context=None):
        """Переопределяем список записей"""
        obj = Intro.objects.first()

        if obj is not None:
            url = reverse('admin:levels_intro_change', args=[obj.id])
            return HttpResponseRedirect(url)
        else:
            url = reverse('admin:levels_intro_add')
            return HttpResponseRedirect(url)

    def has_add_permission(self, request):
        """Запрещаем создание новой записи, если уже есть одна"""
        if Intro.objects.exists():
            return False
        return super().has_add_permission(request)