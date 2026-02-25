from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.stage import Stage


class StagePrize(models.Model):
    stage = models.ForeignKey(Stage, verbose_name=_('Stage'), on_delete=models.CASCADE)

    image = models.ImageField(verbose_name=_('Image'), upload_to='stage_prizes')
    mini_image = models.ImageField(verbose_name=_('Mini Image'), upload_to='stage_prizes')
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)
    requirement = models.TextField(_('Requirement'), null=True, blank=True)
    count = models.IntegerField(_('Count'), null=True, blank=True)