from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserGames(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='games')

    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Started At'))
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Ended At'))
    paused_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Paused At'))
    pause_duration = models.IntegerField(null=True, verbose_name=_('Pause Duration'))
    quest_completed = models.BooleanField(null=True, verbose_name=_('Quests Completed'))
    status = models.SmallIntegerField(null=True, verbose_name=_('Status'))
    is_quest = models.BooleanField(default=False, verbose_name=_('Is Quest'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

class CouponModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='coupon',
    )
    number = models.CharField(verbose_name=_('Coupon Number'), max_length=20, null=True, blank=True)
    description = models.CharField(verbose_name=_('Description'), max_length=255, null=True, blank=True)
    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True)
    created = models.BooleanField(verbose_name=_('Created'), default=False)
    status = models.SmallIntegerField(null=True, verbose_name=_('Status'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))


    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
