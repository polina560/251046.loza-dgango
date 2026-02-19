from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
import uuid
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
    position = models.IntegerField(verbose_name=_('Position'), default=0, null=True)
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


class MediaModel(models.Model):
    # Полиморфная связь (morphs)
    model_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('Model Type'),
        null=True,
        blank=True
    )
    model_id = models.PositiveIntegerField(
        verbose_name=_('Model ID'),
        null=True,
        blank=True
    )
    model = GenericForeignKey('model_type', 'model_id')

    # UUID
    uuid = models.UUIDField(
        verbose_name=_('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=True,
        blank=True
    )

    # Основные поля
    collection_name = models.CharField(
        verbose_name=_('Collection Name'),
        max_length=255
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255
    )
    file_name = models.CharField(
        verbose_name=_('File Name'),
        max_length=255
    )
    mime_type = models.CharField(
        verbose_name=_('MIME Type'),
        max_length=255,
        null=True,
        blank=True
    )
    disk = models.CharField(
        verbose_name=_('Disk'),
        max_length=255
    )
    conversions_disk = models.CharField(
        verbose_name=_('Conversions Disk'),
        max_length=255,
        null=True,
        blank=True
    )
    size = models.PositiveBigIntegerField(
        verbose_name=_('Size')
    )

    # JSON поля
    manipulations = models.JSONField(
        verbose_name=_('Manipulations'),
        default=dict
    )
    custom_properties = models.JSONField(
        verbose_name=_('Custom Properties'),
        default=dict
    )
    generated_conversions = models.JSONField(
        verbose_name=_('Generated Conversions'),
        default=dict
    )
    responsive_images = models.JSONField(
        verbose_name=_('Responsive Images'),
        default=dict
    )

    # Порядок
    order_column = models.PositiveIntegerField(
        verbose_name=_('Order Column'),
        null=True,
        blank=True,
        db_index=True
    )

    # Временные метки
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Media')

        # Индексы для производительности
        indexes = [
            models.Index(fields=['model_type', 'model_id']),
            models.Index(fields=['collection_name']),
            models.Index(fields=['disk']),
            models.Index(fields=['order_column']),
            models.Index(fields=['created_at']),
        ]

        # Сортировка по умолчанию
        ordering = ['order_column', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.file_name})"

    # @property
    # def url(self):
    #     """Получить URL файла"""
    #     from django.core.files.storage import
    #     storage_class = get_storage_class()
    #     storage = storage_class()
    #     return storage.url(self.file_name)
    #
    # @property
    # def path(self):
    #     """Получить путь к файлу"""
    #     from django.core.files.storage import get_storage_class
    #     storage_class = get_storage_class()
    #     storage = storage_class()
    #     return storage.path(self.file_name)
    #
    # @property
    # def extension(self):
    #     """Получить расширение файла"""
    #     import os
    #     return os.path.splitext(self.file_name)[1].lower()
    #
    # @property
    # def is_image(self):
    #     """Проверить, является ли файл изображением"""
    #     return self.mime_type and self.mime_type.startswith('image/')
    #
    # @property
    # def is_video(self):
    #     """Проверить, является ли файл видео"""
    #     return self.mime_type and self.mime_type.startswith('video/')
    #
    # @property
    # def is_audio(self):
    #     """Проверить, является ли файл аудио"""
    #     return self.mime_type and self.mime_type.startswith('audio/')
    #
    # @property
    # def is_document(self):
    #     """Проверить, является ли файл документом"""
    #     document_types = [
    #         'application/pdf',
    #         'application/msword',
    #         'application/vnd.openxmlformats-officedocument',
    #         'text/plain'
    #     ]
    #     return any(self.mime_type.startswith(dt) for dt in document_types) if self.mime_type else False

