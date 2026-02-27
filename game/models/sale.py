from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from game.models.media import Media


class Sale(models.Model):
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')

    def __str__(self):
        return self.title

    @property
    def images(self):
        return Media.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id)

    def add_image(self, file, custom_properties=None):
        """
        Добавляет изображение к акции.
        """
        from .media import Media

        return Media.objects.create(
            model=self,
            collection_name='images',
            file_name=file.name,
            mime_type=file.content_type,
            size=file.size,
            disk=getattr(settings, 'DEFAULT_FILE_STORAGE', 'public'),
            custom_properties=custom_properties or {},
            order_column=self.images.count() + 1
        )

    def clear_images(self):
        """
        Удаляет все изображения акции.
        """
        self.images.delete()

    def get_first_image(self):
        """
        Возвращает первое изображение.
        """
        return self.images.first()

    def register_media_collections(self):
        """
        Регистрирует коллекции медиа.
        """
        # В Django мы не регистрируем коллекции заранее,
        # а просто фильтруем по collection_name при запросе
        pass