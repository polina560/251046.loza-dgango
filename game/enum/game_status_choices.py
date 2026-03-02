from django.db import models
from django.utils.translation import gettext_lazy as _


class GameStatus(models.IntegerChoices):
    NEW = 0, _('new')
    COMPLETED = 1, _('completed')
    ABORTED = 2, _('aborted')
    PAUSED = 3, _('paused')

    @property
    def description(self):
        return self.label