from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.bonus_item import BonusItem


class BonusItemLog(models.Model):
    bonus_item = models.ForeignKey(BonusItem, related_name='bonus_item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bonus_item', on_delete=models.CASCADE)
    source = models.IntegerField(verbose_name=_('Source'), null=True, blank=True)
    is_reserve = models.BooleanField(verbose_name=_('Is reserve'), default=False)

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Bonus item source')
        verbose_name_plural = _('Bonus items source')

    @classmethod
    def add_log(cls, user_id, item_id, source, is_reserve=False):
            return cls.objects.create(
                user_id=user_id,
                bonus_item_id=item_id,
                source=source,
                is_reserve=is_reserve)