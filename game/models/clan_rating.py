from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.clan import Clan
from game.models.stage import Stage


class ClanRating(models.Model):
    clan = models.ForeignKey(
        Clan,
        on_delete=models.CASCADE,
        verbose_name=_('Clan'),
        related_name='clan_ratings',
    )

    stage = models.ForeignKey(
        Stage,
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

    class Meta:
        verbose_name = _('Clan rating')
        verbose_name_plural = _('Clans rating')

    def order_by_rating(self):
        return self.order_by('-total_glory')

