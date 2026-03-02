from django.db import models
from django.utils.translation import gettext_lazy as _


class GamePlatform(models.IntegerChoices):
    SITE = 0, _('site')
    APPLICATION = 1, _('application')

    @property
    def description(self):
        return self.label