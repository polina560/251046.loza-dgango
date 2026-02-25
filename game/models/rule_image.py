
from django.db import models
from django.utils.translation import gettext_lazy as _



class RuleImage(models.Model):
    position = models.IntegerField(verbose_name=_('Position'), default=0)
    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True)

    class Meta:
        verbose_name = _('Rule Image')
        verbose_name_plural = _('Rule Images')