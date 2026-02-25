from django.db import models
from django.utils.translation import gettext_lazy as _


class Text(models.Model):
    key = models.CharField(verbose_name=_('Key'), max_length=255, unique=True)
    # TODO: поле text изменить на value
    text = models.TextField(verbose_name=_('Value'), max_length=2000)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True )

    class Meta:
        verbose_name = _('Text')  # Название в единственном числе
        verbose_name_plural = _('Texts')  # Название во множественном числе

    def __str__(self):
        return self.key