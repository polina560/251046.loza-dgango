from rest_framework import serializers


class RulesSerializer(serializers.Serializer):
    """
    Сериализатор, преобразующий коллекцию RuleImage в список URL изображений,
    отсортированных по позиции.
    """

    def to_representation(self, instance):
        """
        Преобразует queryset RuleImage в список URL изображений.

        Args:
            instance: QuerySet или список объектов RuleImage

        Returns:
            list: Список URL изображений, отсортированных по позиции
        """
        # Получаем все объекты, отсортированные по позиции
        if hasattr(instance, 'all'):
            items = instance.all().order_by('position')
        else:
            items = sorted(instance, key=lambda x: x.position)

        # Формируем список URL
        result = []
        request = self.context.get('request')

        for rule_image in items:
            if rule_image.image:
                if request:
                    url = request.build_absolute_uri(rule_image.image.url)
                else:
                    url = rule_image.image.url
                result.append(url)

        return result


class RulesField(serializers.Field):
    """
    Кастомное поле, которое преобразует queryset RuleImage в список URL изображений.
    """

    def to_representation(self, value):
        """
        Преобразует связанные RuleImage в список URL.

        Args:
            value: QuerySet объектов RuleImage или related manager

        Returns:
            list: Список URL изображений
        """
        if hasattr(value, 'all'):
            items = value.all().order_by('position')
        else:
            items = value.order_by('position') if hasattr(value, 'order_by') else value

        result = []
        request = self.context.get('request')

        for rule_image in items:
            if rule_image.image:
                if request:
                    url = request.build_absolute_uri(rule_image.image.url)
                else:
                    url = rule_image.image.url
                result.append(url)

        return result