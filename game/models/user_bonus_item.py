import random
from asyncio.windows_events import NULL
from xml.dom import ValidationErr

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from httpx import RequestError

from game.enum.bonus_item_log_choices import BonusItemLogChoices
from game.models.bonus_item import BonusItem
from game.models.bonus_item_log import BonusItemLog
from game.models.coupon import Coupon
from game.services.bristol_api import bristol_api


class UserBonusItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonus_items')
    bonus = models.ForeignKey(BonusItem, on_delete=models.CASCADE, related_name='bonus_items')

    count = models.IntegerField(null=True, verbose_name=_('Count'))
    buy_count = models.IntegerField(null=True, verbose_name=_('Buy Count'))
    drop_count = models.IntegerField(null=True, verbose_name=_('Drop Count'))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'bonus'],
                name='unique_user_bonus_item'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'bonus']),
            models.Index(fields=['count']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.bonus.title} (x{self.count or 0})"

    def activate(self, skip_coupon=False):
        """
        Активирует предмет пользователя.

        Args:
            skip_coupon: пропускать ли купоны (для коробок)

        Returns:
            Результат активации (для коробок) или None

        Raises:
            ValidationError: если нет предметов для активации
        """
        # Проверки
        user_extra = self.user.extra
        if not self.count or not self.bonus or not user_extra:
            raise ValidationError('Нет предметов для активации')

        bonus = self.bonus
        result = None

        # Обработка в зависимости от системного имени
        system_name = bonus.system_name

        if system_name == 'box':
            result = self._open_box(skip_coupon)
        elif system_name == 'glory':
            user_extra.add_glory(bonus.reward)
        elif system_name == 'money':
            user_extra.add_money(bonus.reward)
        elif system_name == 'contract':
            user_extra.bonus_quests += bonus.reward
        elif system_name in ['health', 'strength', 'vitality']:
            current_value = getattr(user_extra, system_name)
            setattr(user_extra, system_name, current_value + bonus.reward)


        self.count -= 1
        self.save()
        user_extra.save()

        return result

    def _open_box(self, skip_coupon=False):
        """
        Открывает коробку с предметами.

        Args:
            skip_coupon: если True, исключает предметы 'not_game_prize' из выпадения

        Returns:
            Выпавший предмет или результат выдачи купона
        """
        if not self.bonus:
            return None

        # Получаем все предметы-коробки
        query = BonusItem.objects.filter(is_box=True)
        if skip_coupon:
            query = query.exclude(system_name='not_game_prize')

        items = list(query)
        if not items:
            return None

        # Расчёт шансов выпадения
        chance_sum = 1
        item_ranges = {self.bonus.pk: (1, chance_sum)}

        for item in items:
            item_ranges[item.pk] = (chance_sum + 1, chance_sum + (item.chance or 0))
            chance_sum += (item.chance or 0)

        # Выбираем случайный предмет
        random_value = random.randint(1, chance_sum)
        dropped_item = None

        for item_id, (start, end) in item_ranges.items():
            if start <= random_value <= end:
                dropped_item = next((item for item in items if item.pk == item_id), None)
                break

        # Если ничего не выпало по шансам, выбираем случайный
        if not dropped_item:
            dropped_item = random.choice(items)

        result = dropped_item

        # Обработка выпавшего предмета
        if dropped_item.system_name == 'not_game_prize':
            # Выдаём купон
            result = self._issue_coupon()
        else:
            # Получаем или создаём запись предмета у пользователя
            user_item, created = UserBonusItems.objects.get_or_create(
                user=self.user,
                bonus=dropped_item,
                defaults={'count': 0, 'buy_count': 0, 'drop_count': 0}
            )

            # Увеличиваем счётчики
            user_item.count += 1
            user_item.drop_count += 1

            # Если предмет активируется сразу (не коробка)
            if dropped_item.system_name in [
                'contract', 'glory', 'money', 'health', 'strength', 'vitality'
            ]:
                # Сохраняем перед активацией? В оригинале вызывается instanceActivate()
                # который внутри вызывает activate() для этого же предмета
                # Нужно быть осторожным, чтобы избежать рекурсии
                if hasattr(user_item, 'instance_activate'):
                    user_item.instance_activate()
                else:
                    user_item.save()
            else:
                user_item.save()

            # Логируем
            BonusItemLog.add_log(
                user_id=self.user.pk,
                item_id=dropped_item.pk,
                source=BonusItemLogChoices.SOURCE_BOX,
                is_reserve=skip_coupon
            )

        return result

    def _issue_coupon(self):
        """
        Выдаёт купон пользователю через внешний API.

        Returns:
            Данные купона или результат повторного открытия коробки без купона
        """
        if not self.user:
            raise ValidationError('Нет пользователя')


        try:
            # Вызов внешнего API
            result = bristol_api.issue_coupon(self.user.profile.uid)

            # Проверяем, является ли результат числом (код ошибки)
            if isinstance(result, int):
                if result >= 500:
                    # Серверная ошибка - создаём запись о неудаче
                    Coupon.objects.create(
                        user=self.user,
                        created=False,
                        status=result
                    )
                    # Возвращаем заглушку
                    result = {
                        'number': None,
                        'description': None,
                        'image_url': None,
                        'created': False,
                        'system_name': 'coupon',
                    }
                else:
                    # Другие ошибки - пробуем открыть коробку без купона
                    result = self._open_box(skip_coupon=True)
            else:
                # Успешный ответ - создаём запись о купоне
                Coupon.objects.create(
                    user=self.user,
                    number=result.get('number'),
                    description=result.get('description'),
                    image=result.get('image_url'),
                    created=result.get('created', False),
                    status=200
                )
                result['system_name'] = 'coupon'

        except ConnectionError as e:
            # Ошибка соединения - логируем и пробуем открыть коробку без купона
            # logger.error(f"Bristol API connection error: {e}")
            result = self._open_box(skip_coupon=True)
        except Exception as e:
            # Другие непредвиденные ошибки
            # logger.error(f"Unexpected error in issue_coupon: {e}")
            result = self._open_box(skip_coupon=True)

        return result

    @classmethod
    def get_or_create(cls, user_id, bonus_item_id):
        """
        Получает или создаёт запись о предмете пользователя.
        Аналог getOrCreate в Laravel.
        """
        obj, created = cls.objects.get_or_create(
            user_id=user_id,
            bonus_id=bonus_item_id,
            defaults={'count': 0, 'buy_count': 0, 'drop_count': 0}
        )
        return obj

    def instance_activate(self):
        if (self.count and self.bonus.system_name in [
                'contract',
                'glory',
                'money',
                'health',
                'strength',
                'vitality']):
            self.activate()
