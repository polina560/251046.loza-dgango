from django.db import models
from django.utils.translation import gettext_lazy as _


class BonusItemLogChoices(models.IntegerChoices):
    SOURCE_SHOP = 0, _('source_shop')
    SOURCE_IN_GAME = 1, _('source_in_game')
    SOURCE_CHECK = 2, _('source_check')
    SOURCE_BOX = 3, _('source_box')

    @property
    def description(self):
        """Возвращает описание (как метод description() в Laravel)"""
        return self.label