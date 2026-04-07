from django.db import models
from django.utils.translation import gettext_lazy as _

class Intro(models.Model):
    cyclic_video = models.FileField(verbose_name=_('Cyclic Video'), max_length=255, null=True)
    background_video = models.FileField(verbose_name=_('Processing Video'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Intro')
        verbose_name_plural = _('Intro')

    def __str__(self):
        return str(self.id)


class IntroDialogue(models.Model):
    intro_id = models.ForeignKey(Intro, verbose_name=_('Intro ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Dialogue')
        verbose_name_plural = _('Dialogue')

    def __str__(self):
        return str(self.id)