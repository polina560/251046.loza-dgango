from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

from game.models.bonus_item import BonusItem
from game.models.stage import Stage
from game.models.user_extra import UserExtra
from game.models.user_rating import UserRating
from game.serializers.bonus_item_serializer import BonusItemSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля пользователя, аналог Laravel ProfileResource
    """
    # Поля из UserExtra
    tutorial_completed = serializers.BooleanField(source='extra.tutorial_completed', read_only=True)
    money = serializers.IntegerField(source='extra.money', read_only=True)
    health = serializers.IntegerField(source='extra.health', read_only=True)
    strength = serializers.IntegerField(source='extra.strength', read_only=True)
    vitality = serializers.IntegerField(source='extra.vitality', read_only=True)
    share_used = serializers.BooleanField(source='extra.share_used', read_only=True)
    quests = serializers.SerializerMethodField()
    quests_cooldown = serializers.IntegerField(source='extra.quests_cooldown', read_only=True)
    damage_dealt = serializers.IntegerField(source='extra.damage_dealt', read_only=True)
    damage_taken = serializers.IntegerField(source='extra.damage_taken', read_only=True)

    # Поля из UserProfile
    id = serializers.CharField(source='profile.uid', read_only=True)
    rid = serializers.CharField(source='profile.rid', read_only=True)
    clan = serializers.SerializerMethodField()
    referral_code = serializers.CharField(source='profile.referral_code', read_only=True)

    # Поля из связанных моделей
    glory = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    referred = serializers.SerializerMethodField()
    referred_left = serializers.SerializerMethodField()
    referred_by = serializers.SerializerMethodField()

    # Стандартное поле User
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'rid', 'username', 'tutorial_completed', 'money', 'glory',
            'health', 'strength', 'vitality', 'share_used', 'quests',
            'quests_cooldown', 'damage_dealt', 'damage_taken', 'clan',
            'inventory', 'referral_code', 'referred', 'referred_left', 'referred_by'
        ]

    def get_quests(self, obj):
        """Общее количество доступных квестов"""
        try:
            extra = obj.extra
            # Перед вычислением вызываем генерацию квестов
            extra.calc_quests_generation()
            return (extra.quests or 0) + (extra.bonus_quests or 0)
        except UserExtra.DoesNotExist:
            return 0

    def get_glory(self, obj):
        """Текущая слава пользователя"""
        try:
            # Получаем текущий этап
            current_stage = Stage.objects.filter(
                start_at__lte=timezone.now()
            ).order_by('-start_at').first()

            if not current_stage:
                return 0

            # Получаем рейтинг пользователя на текущем этапе
            rating = UserRating.objects.filter(
                user=obj,
                stage=current_stage
            ).first()

            return rating.glory if rating else 0
        except:
            return 0

    def get_clan(self, obj):
        """Системное имя клана пользователя"""
        try:
            clan = obj.profile.clan
            return clan.system_name if clan else None
        except:
            return None

    def get_inventory(self, obj):
        """
        Формирует инвентарь пользователя: все бонусные предметы магазина
        с количеством, купленным и выпавшим у пользователя
        """
        # Получаем все предметы магазина, отсортированные по позиции
        shop_items = BonusItem.objects.filter(is_shop=True).order_by('position')

        # Получаем все предметы пользователя
        user_items = {item.bonus_id: item for item in obj.bonus_items.all()}

        inventory = []
        request = self.context.get('request')

        for item in shop_items:
            # Сериализуем базовую информацию о предмете
            item_data = BonusItemSerializer(instance=item, context={'request': request}).data

            # Добавляем пользовательские данные
            user_item = user_items.get(item.id)
            item_data['count'] = user_item.count if user_item else 0
            item_data['buy_count'] = user_item.buy_count if user_item else 0
            item_data['drop_count'] = user_item.drop_count if user_item else 0

            inventory.append(item_data)

        return inventory

    def get_referred(self, obj):
        """
        Количество рефералов пользователя за текущий этап
        """
        try:
            current_stage = Stage.objects.filter(
                start_at__lte=timezone.now()
            ).order_by('-start_at').first()

            if not current_stage:
                return 0

            return User.objects.filter(
                profile__referred_by=obj,
                profile__referred_at__range=[current_stage.start_at, current_stage.end_at]
            ).count()
        except:
            return 0

    def get_referred_left(self, obj):
        """
        Осталось пригласить рефералов до максимума
        """
        max_per_stage = getattr(settings, 'REFERRAL_MAX_PER_STAGE', 5)  # значение по умолчанию
        referred = self.get_referred(obj)
        return max(0, max_per_stage - referred)

    def get_referred_by(self, obj):
        """
        Информация о пользователе, который пригласил текущего
        """
        try:
            referred_by_user = obj.profile.referred_by
            if not referred_by_user:
                return None

            return {
                'id': referred_by_user.profile.uid if hasattr(referred_by_user, 'profile') else None,
                'rid': referred_by_user.profile.rid if hasattr(referred_by_user, 'profile') else None,
                'username': referred_by_user.username,
                'clan': referred_by_user.profile.clan.system_name if
                (hasattr(referred_by_user, 'profile') and referred_by_user.profile.clan) else None,
            }
        except:
            return None

    def to_representation(self, instance):
        """
        Дополнительная обработка перед возвратом данных
        """
        # Проверяем наличие UserExtra, создаём если нет
        try:
            extra = instance.extra
        except UserExtra.DoesNotExist:
            # Создаём UserExtra с значениями по умолчанию
            extra = UserExtra.objects.create(
                user=instance,
                health=1,
                strength=1,
                vitality=1,
                money=0,
                quests=0,
                bonus_quests=0,
                tutorial_completed=False,
                share_used=False,
                damage_dealt=0,
                damage_taken=0,
                block_count=0,
                code_fail_count=0,
                money_gain=0,
                money_spent=0
            )

        # Проверяем наличие реферального кода, генерируем если нет
        try:
            profile = instance.profile
            if not profile.referral_code:
                profile.generate_referral_code()
        except:
            pass

        # Получаем стандартное представление
        data = super().to_representation(instance)

        # Ограничиваем значения характеристик максимальным значением
        max_stat = getattr(User, 'MAX_STAT', 4)
        data['health'] = min(data['health'], max_stat)
        data['strength'] = min(data['strength'], max_stat)
        data['vitality'] = min(data['vitality'], max_stat)

        return data