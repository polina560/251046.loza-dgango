# serializers.py
from rest_framework import serializers

from .models import UserGames, GamePlatform


class UserGamesSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = UserGames
        fields = ['id', 'status', 'status_display', 'platform', 'platform_display',
                  'started_at', 'ended_at', 'paused_at', 'pause_duration',
                  'quest_completed', 'is_quest', 'duration', 'created_at']

    def get_duration(self, obj):
        """Получить длительность игры в секундах"""
        return obj.duration


class GameStateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField(allow_null=True)
    paused_at = serializers.DateTimeField(allow_null=True)
    pause_duration = serializers.IntegerField()
    quest_completed = serializers.BooleanField()
    status = serializers.CharField()
    platform = serializers.CharField()
    is_quest = serializers.BooleanField()