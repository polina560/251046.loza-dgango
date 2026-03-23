# game/views/item_controller.py
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from game.models.bonus_item import BonusItem
from game.models.user_bonus_item import UserBonusItems
from game.serializers.bonus_item_serializer import BonusItemSerializer
from game.serializers.profile_serializer import ProfileSerializer

logger = logging.getLogger(__name__)


class ItemShopView(APIView):
    """
    Список доступных к покупке предметов.
    GET /api/item/shop
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Список товаров в магазине",
        description="Возвращает список всех предметов, доступных для покупки в магазине",
        tags=['Item'],
        responses={
            200: {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'example': {
                            'items': [
                                {
                                    'system_name': 'health_1',
                                    'title': 'Здоровье +1',
                                    'description': 'Увеличивает здоровье на 1',
                                    'price': 100,
                                    'reward': 1
                                }
                            ]
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        items = BonusItem.objects.filter(is_shop=True).order_by('position')

        # Выбираем только нужные поля, как в Laravel
        items = items.only('system_name', 'title', 'description', 'price', 'reward')

        serializer = BonusItemSerializer(items, many=True, context={'request': request})

        return Response({
            'items': serializer.data
        })


class ItemBuyView(APIView):
    """
    Приобрести предмет в магазине.
    POST /api/item/buy
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Приобрести предмет",
        description="Покупка предмета в магазине за игровую валюту",
        tags=['Item'],
        request={
            'application/json': {
                'type': 'object',
                'required': ['system_name'],
                'properties': {
                    'system_name': {
                        'type': 'string',
                        'description': 'System Name предмета',
                        'example': 'health_1'
                    }
                }
            }
        },
        responses={
            200: {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'example': {
                            'message': 'Предмет приобретен',
                            'profile': {},
                            'count': 5
                        }
                    }
                }
            },
            400: {
                'description': 'Bad Request',
                'content': {
                    'application/json': {
                        'example': {'error': 'Предмет недоступен для покупки'}
                    }
                }
            },
            404: {
                'description': 'Not Found',
                'content': {
                    'application/json': {
                        'example': {'error': 'Предмет не найден'}
                    }
                }
            }
        }
    )
    def post(self, request):
        system_name = request.data.get('system_name')

        if not system_name:
            return Response(
                {'error': 'Не указан ID предмета'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем предмет по system_name
        try:
            item = BonusItem.objects.get(system_name=system_name)
        except BonusItem.DoesNotExist:
            return Response(
                {'error': 'Предмет не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        try:
            # Вызываем метод покупки у модели BonusItem
            user_item = item.buy(user)

            # Сериализуем профиль пользователя
            profile_serializer = ProfileSerializer(user, context={'request': request})

            return Response({
                'message': 'Предмет приобретен',
                'profile': profile_serializer.data,
                'count': user_item.count
            })

        except Exception as e:
            logger.error(f"Error buying item: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ItemActivateView(APIView):
    """
    Активировать предмет (использовать).
    POST /api/item/activate
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Активировать предмет",
        description="Использование предмета из инвентаря (открытие сундука, лечение и т.д.)",
        tags=['Item'],
        request={
            'application/json': {
                'type': 'object',
                'required': ['id'],
                'properties': {
                    'id': {
                        'type': 'string',
                        'description': 'System Name предмета',
                        'example': 'box_gold'
                    }
                }
            }
        },
        responses={
            200: {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'example': {
                            'message': 'Предмет использован',
                            'profile': {},
                            'count': 2,
                            'drop': {
                                'system_name': 'health_1',
                                'title': 'Здоровье +1',
                                'description': 'Увеличивает здоровье на 1',
                                'price': 0,
                                'reward': 1
                            }
                        }
                    }
                }
            },
            400: {
                'description': 'Bad Request',
                'content': {
                    'application/json': {
                        'example': {'error': 'Нет предметов для активации'}
                    }
                }
            },
            404: {
                'description': 'Not Found',
                'content': {
                    'application/json': {
                        'example': {'error': 'Предмет не найден'}
                    }
                }
            }
        }
    )
    def post(self, request):
        system_name = request.data.get('id')

        if not system_name:
            return Response(
                {'error': 'Не указан ID предмета'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем предмет по system_name
        try:
            item = BonusItem.objects.get(system_name=system_name)
        except BonusItem.DoesNotExist:
            return Response(
                {'error': 'Предмет не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        # Получаем или создаем запись предмета у пользователя
        user_item = UserBonusItems.get_or_create(
            user_id=user.id,
            bonus_item_id=item.id
        )

        if user_item.count <= 0:
            return Response(
                {'error': 'Нет предметов для активации'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Активируем предмет
            drop = user_item.activate()

            # Сериализуем профиль пользователя
            profile_serializer = ProfileSerializer(user, context={'request': request})

            # Подготавливаем ответ
            response_data = {
                'message': 'Предмет использован',
                'profile': profile_serializer.data,
                'count': user_item.count
            }

            # Если есть дроп (для сундуков), добавляем его
            if drop is not None:
                if isinstance(drop, BonusItem):
                    response_data['drop'] = BonusItemSerializer(
                        drop, context={'request': request}
                    ).data
                else:
                    # Если дроп - словарь (например, данные купона)
                    response_data['drop'] = drop

            return Response(response_data)

        except Exception as e:
            logger.error(f"Error activating item: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# Объединяем все views в один контроллер (опционально)
class ItemController(APIView):
    """
    Общий контроллер для работы с предметами.
    Можно использовать один endpoint с параметром action.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == 'shop':
            return ItemShopView().get(request)
        return Response(
            {'error': 'Invalid action'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, action=None):
        if action == 'buy':
            return ItemBuyView().post(request)
        elif action == 'activate':
            return ItemActivateView().post(request)
        return Response(
            {'error': 'Invalid action'},
            status=status.HTTP_400_BAD_REQUEST
        )