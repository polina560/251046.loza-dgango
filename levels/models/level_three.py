from django.db import models
from django.utils.translation import gettext_lazy as _


class LevelThree(models.Model):
    process_video = models.FileField(verbose_name=_('Process Video'), max_length=255, null=True)
    cyclic_video = models.FileField(verbose_name=_('Cyclic Video'), max_length=255, null=True)
    final_video = models.FileField(verbose_name=_('Final Video'), max_length=255, null=True)
    reward_video = models.FileField(verbose_name=_('Reward Video'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Level Three')
        verbose_name_plural = _('Level Three')

    def __str__(self):
        return self.id


class LevelThreeDialogue(models.Model):
    level_three_id = models.ForeignKey(LevelThree, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Dialogue Start')
        verbose_name_plural = _('Dialogue Start')

    def __str__(self):
        return self.id

class LevelThreeDialogueExpl(models.Model):
    level_three_id = models.ForeignKey(LevelThree, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Dialogue Expl')
        verbose_name_plural = _('Dialogue Expl')

    def __str__(self):
        return self.id

class LevelThreeInfo(models.Model):
    level_three_id = models.ForeignKey(LevelThree, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Title'), max_length=255, null=True)
    text = models.TextField(verbose_name=_('Text'), null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Info')
        verbose_name_plural = _('Info')

    def __str__(self):
        return self.id


class LevelThreeResults(models.Model):
    level_three_id = models.ForeignKey(LevelThree, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    title = models.TextField(verbose_name=_('Text'), null=True)
    description = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    process_video = models.FileField(verbose_name=_('Process Video'), max_length=255, null=True)
    result_video = models.FileField(verbose_name=_('Result Video'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def __str__(self):
        return self.id

class LevelThreeDialogueEnd(models.Model):

    level_three_id = models.ForeignKey(LevelThree, verbose_name=_('Level ID'), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Text'), null=True)
    image = models.ImageField(verbose_name=_('Image'), max_length=255, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Dialogue End')
        verbose_name_plural = _('Dialogue End')

    def __str__(self):
        return self.id