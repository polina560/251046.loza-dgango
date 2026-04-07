from django.db import models
from django.utils.translation import gettext_lazy as _
from pygments.lexer import default


class LevelTwo(models.Model):
    hint_video = models.FileField(verbose_name=_('Hint Video'), max_length=255, null=True)
    transfer_video = models.FileField(verbose_name=_('Transfer Video'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Level Two')
        verbose_name_plural = _('Level Two')

    def __str__(self):
        return self.id


class LevelTwoDialogue(models.Model):
    level_two_id = models.ForeignKey(LevelTwo, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Dialogue Start')
        verbose_name_plural = _('Dialogue Start')

    def __str__(self):
        return self.id


class LevelTwoDialogueEnd(models.Model):
    class ErrorIndicatorEnum(models.TextChoices):
        Excellent = 'excellent', '0-10%'
        Normal = 'normal', '20-70%'
        Bad = 'bad', '80-100%'

    level_two_id = models.ForeignKey(LevelTwo, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)
    indicator = models.CharField(choices=ErrorIndicatorEnum.choices, default=ErrorIndicatorEnum.Excellent)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Dialogue End')
        verbose_name_plural = _('Dialogue End')

    def __str__(self):
        return self.id