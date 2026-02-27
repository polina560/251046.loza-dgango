import time

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra')

    quests = models.IntegerField(null=True, default=0, verbose_name=_('Quests'))
    bonus_quests = models.IntegerField(null=True, default=0, verbose_name=_('Bonus Quests'))
    quests_updated_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Quests Updated At'))
    money = models.IntegerField(default=0, verbose_name=_('Money'))
    health = models.IntegerField(default=0, verbose_name=_('Health'))
    strength = models.IntegerField(default=0, verbose_name=_('Strength'))
    vitality = models.IntegerField(default=0, verbose_name=_('Vitality'))

    share_used = models.BooleanField(default=False, verbose_name=_('Share Used'))
    damage_dealt = models.IntegerField(default=0, verbose_name=_('Damage Dealt'))
    damage_taken = models.IntegerField(default=0, verbose_name=_('Damage Taken'))
    block_count = models.IntegerField(default=0, verbose_name=_('Block Count'))
    code_fail_count = models.IntegerField(default=0, verbose_name=_('Code Fail Count'))

    money_gain = models.IntegerField(default=0, verbose_name=_('Money Gain'))
    money_spent = models.IntegerField(default=0, verbose_name=_('Money Spent'))

    tutorial_completed = models.BooleanField(default=False, verbose_name=_('Tutorial Completed'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def calc_quests_generation(self):
        from django.utils import timezone
        from django.conf import settings

        base_quests = getattr(settings, 'BASE_QUESTS', 3)

        if not self.quests_updated_at:
            self.quests_updated_at = timezone.now()
            self.quests = base_quests
            self.save()
            return

        if self.quests >= base_quests:
            return

        # Проверяем переход на новый день
        if self.quests_updated_at.date() < timezone.now().date():
            self.quests = base_quests
            self.quests_updated_at = timezone.now()
            self.save()
            return

        if self.quests > 0:
            return

        # Почасовое восстановление
        time_passed = (timezone.now() - self.quests_updated_at).total_seconds()
        cooldown = getattr(settings, 'QUESTS_COOLDOWN_HOURS', 1) * 3600

        if time_passed >= cooldown:
            self.quests += 1
            self.quests_updated_at = timezone.now()
            self.save()

    def quests_cooldown(self):
        """Аналог questsCooldown() в Laravel"""
        from django.utils import timezone
        from django.conf import settings

        if self.quests > 0 or not self.quests_updated_at:
            return 0

        cooldown = getattr(settings, 'QUESTS_COOLDOWN_HOURS', 1) * 3600
        now = timezone.now()

        if self.quests_updated_at > now:
            self.quests_updated_at = now
            self.save()
            return cooldown

        time_passed = (now - self.quests_updated_at).total_seconds()
        return max(int(cooldown - time_passed), 0)

    def complete_quest(self):
        """
        Завершает один квест.
        Аналог completeQuest() в Laravel.

        Returns:
            bool: True если квест успешно завершён
        """
        self.calc_quests_generation()

        # Проверяем, есть ли доступные квесты
        if not (self.quests + self.bonus_quests):
            return False

        # Используем обычные квесты в первую очередь
        if self.quests > 0:
            self.quests_updated_at = timezone.now()
            self.quests -= 1
            update_fields = ['quests', 'quests_updated_at']
        else:
            self.bonus_quests -= 1
            update_fields = ['bonus_quests']

        self.save(update_fields=update_fields)
        return True

    def add_money(self, amount):
        """
        Добавляет деньги пользователю.
        Аналог addMoney() в Laravel.
        """

        self.money += amount
        self.money_gain += amount
        self.save(update_fields=['money', 'money_gain'])
        # Обновляем значения из БД
        self.refresh_from_db()

    def spent_money(self, amount):
        """
        Списание денег у пользователя.
        Аналог spentMoney() в Laravel.
        """

        self.money -= amount
        self.money_spent += amount
        self.save(update_fields=['money', 'money_spent'])
        # Обновляем значения из БД
        self.refresh_from_db()

    def add_glory(self, amount):
        """
        Добавляет славу пользователю.
        Аналог addGlory() в Laravel.
        """

        from game.models.stage import Stage
        from game.models.user_rating import UserRating

        if amount is None:
            return

        # Проверяем наличие клана у пользователя
        if not hasattr(self.user, 'profile') or not self.user.profile.clan_id:
            return

        # Получаем текущий активный этап
        try:
            current_stage = Stage.objects.filter(
                start_at__lte=timezone.now(),
                end_at__gte=timezone.now()
            ).order_by('-start_at').first()

            if not current_stage:
                return
        except:
            return

        clan_id = self.user.profile.clan_id

        # Пытаемся обновить существующую запись рейтинга
        updated = UserRating.objects.filter(
            user=self.user,
            clan_id=clan_id,
            stage=current_stage
        ).update(
            glory=models.F('glory') + amount,
            glory_time=int(time.time())
        )

        # Если записи нет, создаём новую
        if not updated:
            UserRating.objects.create(
                user=self.user,
                clan_id=clan_id,
                stage=current_stage,
                glory=amount,
                glory_time=int(time.time())
            )

        # Синхронизация имён методов для совместимости с Laravel

    calcQuestsGeneration = calc_quests_generation
    questsCooldown = quests_cooldown
    completeQuest = complete_quest
    addMoney = add_money
    spentMoney = spent_money
    addGlory = add_glory