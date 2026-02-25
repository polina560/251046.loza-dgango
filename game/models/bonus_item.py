from django.db import models
from django.utils.translation import gettext_lazy as _


class BonusItem(models.Model):
    position = models.IntegerField(verbose_name=_('Position'))
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    system_name = models.CharField(verbose_name=_('System Name'), max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    price = models.IntegerField(verbose_name=_('Price'), null=True, blank=True)
    reward = models.IntegerField(verbose_name=_('Reward'), null=True, blank=True)
    universal_coupon = models.CharField(verbose_name=_('Universal coupon'), max_length=255, null=True, blank=True)
    is_system = models.BooleanField(verbose_name=_('Is system'), default=False)
    is_shop = models.BooleanField(verbose_name=_('Is shop'), default=False)
    is_box = models.BooleanField(verbose_name=_('Is box'), default=False)
    chance = models.IntegerField(verbose_name=_('Chance'), null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Bonus item')
        verbose_name_plural = _('Bonus items')
        ordering = ['position']  # Сортировка по позиции по умолчанию

    def __str__(self):
        return self.title