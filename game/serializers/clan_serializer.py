from rest_framework import serializers

from game.models.clan import Clan


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = ['id', 'system_name', 'title', 'description', 'image']

    def to_representation(self, instance):
        """
        Преобразует экземпляр модели в словарь для ответа API.
        Для поля image возвращает полный URL, если изображение существует.
        """
        data = super().to_representation(instance)

        # Обработка изображения - возвращаем полный URL
        if instance.image:
            # Если используется стандартное хранилище Django
            request = self.context.get('request')
            if request:
                data['image'] = request.build_absolute_uri(instance.image.url)
            else:
                data['image'] = instance.image.url
        else:
            data['image'] = None

        return data