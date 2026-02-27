from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.enum.bonus_item_log_choices import BonusItemLogChoices
from game.models.bonus_item_log import BonusItemLog
from game.models.user_bonus_item import UserBonusItems


def _check_player_stat(user, stat_name):
    """
    Проверяет, не достигнут ли максимум по характеристике.
    """
    max_stat = getattr(user.profile, 'MAX_STAT', 4)
    current_value = getattr(user.extra, stat_name, 0)

    if current_value >= max_stat:
        raise ValidationError(f'Характеристика {stat_name} уже на максимальном уровне')


class BonusItem(models.Model):
    position = models.IntegerField(verbose_name=_('Position'))
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    system_name = models.CharField(verbose_name=_('System Name'), max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    price = models.IntegerField(verbose_name=_('Price'), null=True, blank=True)
    reward = models.IntegerField(verbose_name=_('Reward'), null=True, blank=True)
    universal_coupon = models.CharField(verbose_name=_('Universal coupon'), max_length=255, null=True, blank=True)
    is_system = models.BooleanField(verbose_name=_('Is system'), default=False)
    is_shop = models.BooleanField(verbose_name=_('Is shop'), default=False)
    is_box = models.BooleanField(verbose_name=_('Is box'), default=False)
    chance = models.IntegerField(verbose_name=_('Chance'), null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Bonus item')
        verbose_name_plural = _('Bonus items')
        ordering = ['position']  # Сортировка по позиции по умолчанию

    def __str__(self):
        return self.title


    def buy(self, user):
        self._check_purchase_availability(user)

        user_item = UserBonusItems.objects.get_or_create(user=user, bonus=self, defaults={'count': 0, 'buy_count': 0, 'drop_count': 0})[0]

        if self.system_name in ['health', 'strength', 'vitality']:
            _check_player_stat(user.extra, self.system_name)

        if self.price and self.price > 0:
            # TODO: добавить в user.extra метод spent_money
            user.extra.spent_money(self.price)
            user.extra.save()

            # Обновление статистики предмета
        user_item.buy_count += 1
        user_item.count += 1

        # TODO: добавить метод instance_activate
        user_item.activate()
        user_item.save()


        # TODO: добавить метод add_log
        BonusItemLog.objects.add_log(
            user_id=user.id,
            item_id=self.id,
            source=BonusItemLogChoices.SOURCE_SHOP.value
        )
        return user_item


    def _check_purchase_availability(self, user):
        """
        Проверяет, может ли пользователь купить этот предмет.
        """
        if not self.is_shop:
            raise ValidationError('Предмет недоступен для покупки')

        try:
            extra = user.extra
        except user.extra.RelatedObjectDoesNotExist:
            raise ValidationError('Данные пользователя не найдены')

        if extra.money < (self.price or 0):
            raise ValidationError('Недостаточно средств')

