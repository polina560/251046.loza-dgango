from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from content.models import ClanModel
from game.models import BonusItemModel
from rating.models import StagePrizesModel


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )

    uid = models.CharField(max_length=255, unique=True, verbose_name='UID')
    rid = models.CharField(max_length=15, unique=True, verbose_name='RID')
    remember_token = models.CharField(max_length=100, null=True, blank=True, verbose_name='Remember Token')

    data = models.JSONField(verbose_name=_('Data'), default=dict, blank=True)

    clan = models.ForeignKey(
        ClanModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name=_('Clan')
    )

    # Реферальная система
    referral_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('Referral Code'),
        unique=True
    )
    referred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals',
        verbose_name=_('Referred by'),
        help_text=_('The user who referred this user'),
        db_column='referred_by_id'
    )
    referred_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Referred At')
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    MAX_STAT = 4

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        indexes = [
            models.Index(fields=['uid'], name='idx_profile_uid'),
            models.Index(fields=['rid'], name='idx_profile_rid'),
            models.Index(fields=['referral_code'], name='idx_profile_ref_code'),
            models.Index(fields=['referred_by'], name='idx_profile_referred_by'),
            models.Index(fields=['clan'], name='idx_profile_clan'),
            models.Index(fields=['referred_at'], name='idx_profile_referred_at'),
            models.Index(fields=['created_at'], name='idx_profile_created'),
        ]

    def __str__(self):
        return f"{self.user.username}'s profile"

class UserBonusItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonus_items')
    bonus = models.ForeignKey(BonusItemModel, on_delete=models.CASCADE, related_name='bonus_items')

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

