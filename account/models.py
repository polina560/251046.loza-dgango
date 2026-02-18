from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from content.models import ClanModel
from game.models import BonusItemModel

# TODO: изменить название таблицы
class UserExt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uid = models.CharField(max_length=255, unique=True, verbose_name='UID')
    rid = models.CharField(max_length=15, unique=True, verbose_name='RID')

    clan = models.OneToOneField(ClanModel, on_delete=models.CASCADE, related_name='extra', null=True)


    def __str__(self):
        return f"{self.user.username}'s profile"

class UserBonusItems(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bonus_items', primary_key=True)
    bonus = models.OneToOneField(BonusItemModel, on_delete=models.CASCADE, related_name='bonus_items', primary_key=True)

    count = models.IntegerField(null=True, verbose_name=_('Count'))
    buy_count = models.IntegerField(null=True, verbose_name=_('Buy Count'))
    drop_count = models.IntegerField(null=True, verbose_name=_('Drop Count'))

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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

class UserGames(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='games')

    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Started At'))
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Ended At'))
    paused_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Paused At'))
    pause_duration = models.IntegerField(null=True, verbose_name=_('Pause Duration'))
    quest_completed = models.BooleanField(null=True, verbose_name=_('Quests Completed'))
    status = models.SmallIntegerField(null=True, verbose_name=_('Status'))
    is_quest = models.BooleanField(default=False, verbose_name=_('Is Quest'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))