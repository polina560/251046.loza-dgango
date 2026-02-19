from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from content.models import ClanModel
from game.models import BonusItemModel
from rating.models import StagePrizesModel


# TODO: изменить название таблицы
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uid = models.CharField(max_length=255, unique=True, verbose_name='UID')
    rid = models.CharField(max_length=15, unique=True, verbose_name='RID')

    remember_token = models.CharField(max_length=100, null=True, verbose_name='Remember Token')

    clan = models.OneToOneField(ClanModel, on_delete=models.CASCADE, related_name='profile', null=True)


    def __str__(self):
        return f"{self.user.username}'s profile"

class UserBonusItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonus_items')
    bonus = models.ForeignKey(BonusItemModel, on_delete=models.CASCADE, related_name='bonus_items')

    count = models.IntegerField(null=True, verbose_name=_('Count'))
    buy_count = models.IntegerField(null=True, verbose_name=_('Buy Count'))
    drop_count = models.IntegerField(null=True, verbose_name=_('Drop Count'))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'bonus'],
                name='unique_user_bonus_item'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.bonus.title} (x{self.count or 0})"

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

class UserStagePrizes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stage_prizes')
    stage_prize = models.OneToOneField(StagePrizesModel, on_delete=models.CASCADE, related_name='stage_prizes')
    received_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Received At'))

