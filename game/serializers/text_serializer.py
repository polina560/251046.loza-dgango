from rest_framework import serializers

from game.models.text import Text


class TextSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Text.
    Возвращает ключ и значение текстовой записи.
    """
    value = serializers.CharField(source='text', read_only=True)

    class Meta:
        model = Text
        fields = ['key', 'value']

    def to_representation(self, instance):
        """
        Дополнительная обработка перед возвратом данных.
        """
        data = super().to_representation(instance)

        # Убеждаемся, что value не None (если нужно)
        if data.get('value') is None:
            data['value'] = ''

        return data