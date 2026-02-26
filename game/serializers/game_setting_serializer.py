from rest_framework import serializers

from game.models.game_setting import GameSetting


class GameSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSetting
        fields = ['name', 'value']