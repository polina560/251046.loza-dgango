from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class TextModel(models.Model):
    key = models.CharField(verbose_name=_('Key'), max_length=255, unique=True)
    # TODO: поле text изменить на value
    text = models.TextField(verbose_name=_('Value'), max_length=2000)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True )

    class Meta:
        verbose_name = _('Text')  # Название в единственном числе
        verbose_name_plural = _('Texts')  # Название во множественном числе

    def __str__(self):
        return self.key

class ClanModel(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255, null=True)
    system_name = models.CharField(verbose_name=_('System Name'), max_length=255, null=True)
    description = models.TextField(verbose_name=_('Description'), max_length=2000, null=True)
    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('Clan')
        verbose_name_plural = _('Clans')

    def __str__(self):
        return self.title

class FAQModel(models.Model):
    position = models.IntegerField(verbose_name=_('Position'), null=True)
    question = models.CharField(verbose_name=_('Question'), max_length=255, null=True)
    answer = models.TextField(verbose_name=_('Answer'), max_length=2000, null=True)

    created_at = models.DateField(verbose_name=_('Created at'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateField(verbose_name=_('Updated at'), null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')

    def __str__(self):
        return self.question

class RuleImageModel(models.Model):
    position = models.IntegerField(verbose_name=_('Position'), default=0)
    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True)

    class Meta:
        verbose_name = _('Rule Image')
        verbose_name_plural = _('Rule Images')
