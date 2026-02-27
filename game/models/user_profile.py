import random
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
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
        """
        Генерирует реферальный код.
        Аналог generateReferralCode() в Laravel.
        """
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        code = ''.join(random.choices(characters, k=5))
        self.referral_code = code
        self.save(update_fields=['referral_code'])

    @property
    def is_referral_available(self) -> bool:
        """
        Проверяет, доступен ли реферальный бонус.
        Аналог isReferralAvailable в Laravel.
        """
        from .stage import Stage

        # Получаем текущий этап
        stage = Stage.current()
        if not stage:
            return False

        # Проверяем, не закончился ли этап
        if stage.end_at and stage.end_at < timezone.now():
            return False

        # Получаем максимальное количество рефералов за этап
        max_per_stage = getattr(settings, 'REFERRAL_MAX_PER_STAGE', 5)

        # Считаем количество рефералов за текущий этап
        referrals_count = User.objects.filter(
            profile__referred_by=self.user,
            profile__referred_at__range=[stage.start_at, stage.end_at]
        ).count()

        return referrals_count < max_per_stage

    def current_glory(self) -> int:
        """
        Возвращает текущую славу пользователя.
        Аналог currentGlory() в Laravel.
        """
        from .stage import Stage
        from .user_rating import UserRating

        if not self.user_id:
            return 0

        try:
            current_stage_id = Stage.cached_current_id()
        except Exception:
            return 0

        rating = UserRating.objects.filter(
            user=self.user,
            stage_id=current_stage_id
        ).first()

        return rating.glory if rating else 0

    def get_referrals_count(self, stage=None) -> int:
        """
        Возвращает количество рефералов пользователя.

        Args:
            stage: конкретный этап (если None, то за всё время)
        """
        queryset = User.objects.filter(profile__referred_by=self.user)

        if stage:
            queryset = queryset.filter(
                profile__referred_at__range=[stage.start_at, stage.end_at]
            )

        return queryset.count()

    def get_referred_by_info(self) -> Optional[dict]:
        """
        Возвращает информацию о пользователе, который пригласил.
        """
        if not self.referred_by:
            return None

        referred_by_profile = self.referred_by.profile

        return {
            'id': referred_by_profile.uid,
            'rid': referred_by_profile.rid,
            'username': self.referred_by.username,
            'clan': referred_by_profile.clan.system_name if referred_by_profile.clan else None,
        }

    # Расширение модели User через свойства
def get_user_profile_properties():
    """
    Добавляет свойства к модели User для доступа к методам профиля.
    """

    @property
    def extra(self):
        """Доступ к UserExtra."""
        from .user_extra import UserExtra
        try:
            return self.extra_rel
        except UserExtra.DoesNotExist:
            return UserExtra.objects.create(user=self)

    @property
    def profile(self):
        """Доступ к UserProfile."""
        try:
            return self.profile_rel
        except UserProfile.DoesNotExist:
            # Автоматическое создание профиля при необходимости
            return UserProfile.objects.create(
                user=self,
                uid=f"UID{self.id}",
                rid=f"RID{self.id}"
            )

    @property
    def current_glory(self):
        """Текущая слава пользователя."""
        return self.profile.current_glory()

    @property
    def is_referral_available(self):
        """Доступность реферального бонуса."""
        return self.profile.is_referral_available

    def generate_referral_code(self):
        """Генерация реферального кода."""
        return self.profile.generate_referral_code()

    # Добавляем свойства к модели User
    User.extra = extra
    User.profile = profile
    User.current_glory = current_glory
    User.is_referral_available = is_referral_available
    User.generate_referral_code = generate_referral_code

# Вызываем функцию для добавления свойств
get_user_profile_properties()