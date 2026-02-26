from rest_framework import serializers

from game.models.user_stage_prize import UserStagePrizes


class UserStagePrizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для полученных пользователем призов этапа.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    rid = serializers.CharField(source='user.profile.rid', read_only=True)
    image = serializers.SerializerMethodField()
    title = serializers.CharField(source='stage_prize.title', read_only=True)
    created_at = serializers.DateTimeField(source='received_at', read_only=True)

    class Meta:
        model = UserStagePrizes
        fields = ['username', 'rid', 'image', 'title', 'created_at']

    def get_image(self, obj):
        """
        Возвращает URL миниатюры изображения приза.
        """
        if obj.stage_prize and obj.stage_prize.mini_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.stage_prize.mini_image.url)
            return obj.stage_prize.mini_image.url
        return None

    def to_representation(self, instance):
        """
        Дополнительная обработка перед возвратом данных.
        """
        data = super().to_representation(instance)

        # Убеждаемся, что обязательные поля не None
        if data.get('username') is None:
            data['username'] = ''

        if data.get('rid') is None:
            data['rid'] = ''

        if data.get('title') is None:
            data['title'] = ''

        return data