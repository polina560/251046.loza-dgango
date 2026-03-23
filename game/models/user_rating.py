from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.clan import Clan
from game.models.stage import Stage


class UserRatingManager(models.Manager):
    """Кастомный менеджер для UserRating."""

    def global_rating(self, stage_id):
        """
        Возвращает глобальный рейтинг пользователей для указанного этапа.
        """
        return self.filter(
            stage_id=stage_id
        ).select_related('user', 'clan')

    def by_clan(self, stage_id, clan_id):
        """
        Возвращает рейтинг пользователей в конкретном клане.
        """
        return self.filter(
            stage_id=stage_id,
            clan_id=clan_id
        ).select_related('user', 'clan')

    def order_by_rating(self):
        """
        Сортировка по рейтингу (по убыванию славы, по возрастанию времени).
        """
        return self.order_by('-glory', 'glory_time')

class UserRating(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='ratings'
    )
    stage = models.OneToOneField(
        Stage,
        on_delete=models.CASCADE,
        verbose_name=_('Stage'),
        related_name='user_ratings'
    )
    clan = models.OneToOneField(
        Clan,
        on_delete=models.CASCADE,
        verbose_name=_('Clan'),
        related_name='user_ratings'
    )
    glory = models.IntegerField(
        verbose_name=_('Glory')
    )
    glory_time = models.BigIntegerField(
        verbose_name=_('Glory Time'),
        help_text=_('Timestamp for sorting')
    )

    objects = UserRatingManager()

    class Meta:
        verbose_name = _('User Rating')
        verbose_name_plural = _('User Ratings')

        indexes = [
            models.Index(fields=['user'], name='idx_user_ratings_user_id'),
            models.Index(fields=['stage'], name='idx_user_ratings_stage_id'),
            models.Index(fields=['clan'], name='idx_user_ratings_clan_id'),

            models.Index(
                fields=['stage', '-glory', 'glory_time'],
                name='idx_user_ratings_global'
            ),
            models.Index(
                fields=['stage', 'clan', '-glory', 'glory_time'],
                name='idx_user_ratings_clan'
            ),
        ]

    def __str__(self):
        return f"{self.user} - Stage {self.stage} - Glory: {self.glory}"



