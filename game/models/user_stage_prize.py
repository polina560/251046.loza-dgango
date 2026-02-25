from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.stage_prize import StagePrize


class UserStagePrizes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stage_prizes')
    stage_prize = models.OneToOneField(StagePrize, on_delete=models.CASCADE, related_name='stage_prizes')
    received_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Received At'))