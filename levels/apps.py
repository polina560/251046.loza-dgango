from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LevelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'levels'

    verbose_name = _('Levels')
    verbose_name_plural = _('Levels')

