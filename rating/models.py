from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from content.models import ClanModel


# Create your models here.

class StagesModel(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    start_at = models.DateField(_('Start Date'), null=True, blank=True)
    end_at = models.DateField(_('End Date'), null=True, blank=True)
    prize_date = models.CharField(_('Prize Date'), max_length=255, null=True, blank=True)
    prize_description = models.TextField(_('Prize Description'), null=True, blank=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')

    def __str__(self):
        return self.title

class StagePrizesModel(models.Model):
    stage = models.OneToOneField(StagesModel, verbose_name=_('Stage'), on_delete=models.CASCADE)

    image = models.ImageField(verbose_name=_('Image'), upload_to='stage_prizes')
    mini_image = models.ImageField(verbose_name=_('Mini Image'), upload_to='stage_prizes')
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    requirement = models.TextField(_('Requirement'), null=True, blank=True)
    count = models.IntegerField(_('Count'), null=True, blank=True)


class UserRatingModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='ratings'
    )
    stage = models.OneToOneField(
        StagesModel,
        on_delete=models.CASCADE,
        verbose_name=_('Stage'),
        related_name='user_ratings'
    )
    clan = models.OneToOneField(
        ClanModel,
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

class ClanRatingModel(models.Model):
    clan = models.OneToOneField(
        ClanModel,
        on_delete=models.CASCADE,
        verbose_name=_('Clan'),
        related_name='clan_ratings',
    )

    stage = models.OneToOneField(
        StagesModel,
        on_delete=models.CASCADE,
        verbose_name=_('Stage'),
        related_name='clan_ratings',
    )

    total_glory = models.IntegerField(verbose_name=_('Total Glory'))

    indexes = [
        models.Index(
            fields=['stage', 'total_glory'],
            name='idx_clan_ratings_stage_total_glory'
        ),
    ]

