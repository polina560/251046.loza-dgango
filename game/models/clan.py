from django.db import models
from django.utils.translation import gettext_lazy as _


class Clan(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255, null=True)
    system_name = models.CharField(verbose_name=_('System Name'), max_length=255, null=True)
    description = models.TextField(verbose_name=_('Description'), max_length=2000, null=True)
    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Clan')
        verbose_name_plural = _('Clans')

    def __str__(self):
        return self.title