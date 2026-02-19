from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from account.models import UserProfile, UserBonusItems, UserExtra


# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
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


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, UserBonusItemsInline, UserExtraInline)

    # Опционально: добавить поля профиля в список отображения пользователей
    list_display = UserAdmin.list_display





# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)