from django.db import models
from django.utils.translation import gettext_lazy as _


class LevelOne(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255, null=True)
    drop_video = models.FileField(verbose_name=_('Drop Video'), max_length=255, null=True)
    separate_video = models.FileField(verbose_name=_('Separate Video'), max_length=255, null=True)

    info = models.TextField(verbose_name=_('Info'), null=True)
    hint = models.TextField(verbose_name=_('Hint'), null=True)

    cyclic_separate_video = models.FileField(verbose_name=_('Cyclic Video'), max_length=255, null=True)
    processing_video = models.FileField(verbose_name=_('Processing Video'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Level One')
        verbose_name_plural = _('Level One')

    def __str__(self):
        return self.title


class LevelOneDialogue(models.Model):
    level_one_id = models.ForeignKey(LevelOne, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Dialogue')
        verbose_name_plural = _('Dialogue')

    def __str__(self):
        return self.id

class LevelOneContainer(models.Model):
    level_one_id = models.ForeignKey(LevelOne, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_('Type'), max_length=255, null=True)
    title = models.CharField(verbose_name=_('Title'), max_length=255, null=True)
    text = models.TextField(verbose_name=_('Text'), null=True)
    info = models.TextField(verbose_name=_('Info'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Container')
        verbose_name_plural = _('Container')

    def __str__(self):
        return self.title

class LevelOneDialogueEnd(models.Model):
    level_one_id = models.ForeignKey(LevelOne, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)
    earthquake = models.BooleanField(verbose_name=_('Earthquake'), default=False)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Dialogue')
        verbose_name_plural = _('Dialogue')

    def __str__(self):
        return self.id