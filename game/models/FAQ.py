
from django.db import models
from django.utils.translation import gettext_lazy as _



class FAQ(models.Model):
    position = models.IntegerField(verbose_name=_('Position'), default=0, null=True)
    question = models.CharField(verbose_name=_('Question'), max_length=255, null=True)
    answer = models.TextField(verbose_name=_('Answer'), max_length=2000, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')

    def __str__(self):
        return self.question