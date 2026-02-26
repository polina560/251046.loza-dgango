from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from game.models.media import Media
from game.models.sale import Sale


class SaleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Sale.
    Возвращает название акции и список URL изображений.
    """
    images = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['title', 'images']

    def get_images(self, obj):
        """
        Получает все медиафайлы, связанные с данной акцией через модель Media.
        Аналог getMedia('images') в Laravel.

        Returns:
            list: Список полных URL изображений
        """
        # Получаем ContentType для модели Sale
        content_type = ContentType.objects.get_for_model(obj)

        # Получаем все медиафайлы, связанные с этой акцией, отсортированные по порядку
        media_items = Media.objects.filter(
            model_type=content_type,
            model_id=obj.id,
            collection_name='images'  # соответствует коллекции 'images' в Laravel
        ).order_by('order_column')  # сортируем по порядку, если нужно

        # Формируем список URL
        request = self.context.get('request')
        image_urls = []

        for media in media_items:
            if media.file_name:
                # Строим полный URL к файлу
                # В зависимости от настроек хранилища, может быть media.file_name.url или свой метод
                if hasattr(media, 'url') and callable(getattr(media, 'url', None)):
                    url = media.url()
                else:
                    # Если в модели Media есть свойство url
                    url = media.url if hasattr(media, 'url') else f"/media/{media.file_name}"

                # Делаем абсолютный URL, если есть request
                if request:
                    url = request.build_absolute_uri(url)

                image_urls.append(url)

        return image_urls

    def to_representation(self, instance):
        """
        Дополнительная обработка перед возвратом данных.
        Убеждаемся, что поле title не None.
        """
        data = super().to_representation(instance)

        # Если title отсутствует, возвращаем пустую строку (как в Laravel)
        if data.get('title') is None:
            data['title'] = ''

        return data