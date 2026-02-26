from rest_framework import serializers
from django.conf import settings


class UserGameSerializer(serializers.Serializer):
    """
    Сериализатор для игровой сессии пользователя.
    Может работать как с моделью UserGames, так и со словарём состояния.
    """
    status = serializers.IntegerField(allow_null=True)
    quest_requirement = serializers.SerializerMethodField()
    quest_completed = serializers.BooleanField(default=False)
    is_quest = serializers.BooleanField(default=False)

    class Meta:
        fields = ['status', 'quest_requirement', 'quest_completed', 'is_quest']

    def get_quest_requirement(self, obj):
        """
        Возвращает требование для контракта из настроек.
        Аналог config('app.game.quest_requirement').
        """
        return getattr(settings, 'QUEST_REQUIREMENT', 0)

    def to_representation(self, instance):
        """
        Преобразует экземпляр (модель или словарь) в представление.
        """
        if isinstance(instance, dict):
            # Работа со словарём (состояние из сессии)
            return {
                'status': instance.get('status'),
                'quest_requirement': self.get_quest_requirement(instance),
                'quest_completed': instance.get('quest_completed', False),
                'is_quest': instance.get('is_quest', False),
            }
        else:
            # Работа с моделью UserGames
            return {
                'status': instance.status,
                'quest_requirement': self.get_quest_requirement(instance),
                'quest_completed': instance.quest_completed,
                'is_quest': instance.is_quest,
            }