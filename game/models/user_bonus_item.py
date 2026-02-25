from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.bonus_item import BonusItem


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