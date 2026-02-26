
from django.db import models
from django.utils.translation import gettext_lazy as _

class Stage(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    start_at = models.DateTimeField(_('Start Date'), null=True, blank=True)
    end_at = models.DateTimeField(_('End Date'), null=True, blank=True)
    prize_date = models.CharField(_('Prize Date'), max_length=255, null=True, blank=True)
    prize_description = models.TextField(_('Prize Description'), null=True, blank=True)

    winners_sent = models.BooleanField(_('Winners Sent'), default=False)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')

    def __str__(self):
        return self.title