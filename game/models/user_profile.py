import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.clan import Clan


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
        Clan,
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

    def generate_referral_code(self):
        """Аналог generateReferralCode() в Laravel"""
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        code = ''.join(random.choices(characters, k=5))
        self.referral_code = code
        self.save()