from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class RatingConfig(AppConfig):
    name = 'rating'

    verbose_name = _('Rating')
    verbose_name_plural = _('Rating')
