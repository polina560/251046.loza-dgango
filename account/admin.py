from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from account.models import UserExt, UserBonusItems, UserExtra


# Register your models here.

class UserExtInline(admin.StackedInline):
    model = UserExt
    can_delete = False
    verbose_name_plural = 'Профиль'

class UserBonusItemsInline(admin.StackedInline):
    model = UserBonusItems
    can_delete = False
    verbose_name_plural = 'Бонусы'

class UserExtraInline(admin.StackedInline):
    model = UserExtra
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'

class UserGamesInline(admin.StackedInline):
    model = UserExtra
    can_delete = False
    verbose_name_plural = 'Игра'


class CustomUserAdmin(UserAdmin):
    inlines = (UserExtInline, UserBonusItemsInline, UserExtraInline, UserGamesInline)

    # Опционально: добавить поля профиля в список отображения пользователей
    list_display = UserAdmin.list_display





# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)