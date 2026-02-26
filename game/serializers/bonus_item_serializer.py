from rest_framework import serializers

from game.models.bonus_item import BonusItem


class BonusItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusItem
        fields = ['system_name', 'title', 'description', 'price', 'reward']

    def to_representation(self, instance):
        """
        Преобразует экземпляр модели в словарь для ответа API.
        Если system_name == 'money', добавляет к нему суффикс с reward.
        """
        data = super().to_representation(instance)
        if instance.system_name == 'money' and instance.reward is not None:
            data['system_name'] = f"{instance.system_name}_{instance.reward}"
        return data