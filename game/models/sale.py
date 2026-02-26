from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.media import Media


class Sale(models.Model):
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')

    def __str__(self):
        return self.title

    @property
    def images(self):
        return Media.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id)