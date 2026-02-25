from django.db import models
from django.utils.translation import gettext_lazy as _

class GameSetting(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    value = models.CharField(_('Value'), max_length=100, null=True)
    description = models.TextField(_('Description'), max_length=100, null=True)

    class Meta:
        verbose_name = _('Game Settings')  # Название в единственном числе
        verbose_name_plural = _('Game Settings')  # Название во множественном числе

    def __str__(self):
        return self.name