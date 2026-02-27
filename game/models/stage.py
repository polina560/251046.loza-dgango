
from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

class Stage(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    start_at = models.DateTimeField(_('Start Date'), null=True, blank=True)
    end_at = models.DateTimeField(_('End Date'), null=True, blank=True)
    prize_date = models.CharField(_('Prize Date'), max_length=255, null=True, blank=True)
    prize_description = models.TextField(_('Prize Description'), null=True, blank=True)

    winners_sent = models.BooleanField(_('Winners Sent'), default=False)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')

    def __str__(self):
        return self.title

    @classmethod
    def current(cls):
        """
        Возвращает текущий этап (самый новый из начавшихся).
        """
        return cls.objects.filter(
            start_at__lte=timezone.now()
        ).order_by('-start_at').first()

    @classmethod
    def cached_current_id(cls, timeout=60):
        """
        Возвращает ID текущего этапа с кешированием.
        """
        cache_key = 'current_stage_id'

        def get_current_id():
            stage = cls.current()
            if stage is None:
                raise Exception('No current stage')
            return stage.id

        # Пытаемся получить из кеша
        stage_id = cache.get_or_set(cache_key, get_current_id, timeout=timeout)

        return stage_id

    @classmethod
    def clear_cache(cls):
        """
        Очищает кеш текущего этапа.
        """
        cache.delete('current_stage_id')
