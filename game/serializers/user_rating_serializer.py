from rest_framework import serializers

from game.models.user_rating import UserRating


class UserRatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рейтинга пользователя.
    Поддерживает опциональное поле position, передаваемое в контексте.
    """
    position = serializers.SerializerMethodField()
    clan_id = serializers.IntegerField(source='clan.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserRating
        fields = ['position', 'clan_id', 'username', 'glory']

    def get_position(self, obj):
        """
        Возвращает позицию из контекста, если она там есть.
        Аналог $this->position в Laravel.
        """
        return self.context.get('position', None)

    def to_representation(self, instance):
        """
        Дополнительная обработка перед возвратом данных.
        """
        data = super().to_representation(instance)

        # Убеждаемся, что username не None
        if data.get('username') is None:
            data['username'] = ''

        return data