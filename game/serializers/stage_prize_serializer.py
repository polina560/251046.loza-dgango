from rest_framework import serializers
from django.conf import settings

from game.models.stage import Stage
from game.models.stage_prize import StagePrize


class StagePrizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для призов этапа.
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = StagePrize
        fields = ['image', 'title', 'description', 'requirement', 'count']

    def get_image(self, obj):
        """
        Возвращает полный URL изображения приза.
        """
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class StageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для этапа игры.
    Включает связанные призы этапа.
    """
    stagePrizes = serializers.SerializerMethodField()
    start_at = serializers.SerializerMethodField()
    end_at = serializers.SerializerMethodField()

    class Meta:
        model = Stage
        fields = [
            'id', 'title', 'prize_date', 'prize_description',
            'start_at', 'end_at', 'stagePrizes'
        ]

    def get_stagePrizes(self, obj):
        """
        Возвращает список призов для данного этапа.
        Аналог map в Laravel.
        """
        prizes = obj.prizes.all()  # предполагается related_name='prizes' в StagePrize
        serializer = StagePrizeSerializer(
            prizes,
            many=True,
            context=self.context
        )
        return serializer.data

    def get_start_at(self, obj):
        """
        Возвращает временную метку начала этапа.
        В Laravel start_at может быть объектом Carbon, преобразуется автоматически.
        В Django возвращаем timestamp или ISO формат в зависимости от требований.
        """
        if obj.start_at:
            # Если API ожидает timestamp (integer)
            return int(obj.start_at.timestamp())
            # Если API ожидает строку ISO 8601:
            # return obj.start_at.isoformat()
        return None

    def get_end_at(self, obj):
        """
        Возвращает временную метку окончания этапа.
        """
        if obj.end_at:
            return int(obj.end_at.timestamp())
            # return obj.end_at.isoformat()
        return None

    def to_representation(self, instance):
        """
        Дополнительная обработка перед возвратом данных.
        """
        data = super().to_representation(instance)

        # Убеждаемся, что поля не None (если нужно)
        if data.get('prize_date') is None:
            data['prize_date'] = ''

        if data.get('prize_description') is None:
            data['prize_description'] = ''

        return data