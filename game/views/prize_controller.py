from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.user_stage_prize import UserStagePrizes
from game.serializers.user_stage_prize_serializer import UserStagePrizeSerializer


class PrizeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Список полученных призов",
        description="Возвращает список всех полученных призов, отсортированных по дате получения.",
        tags=['Prizes'],
        parameters=[
            OpenApiParameter(
                name='limit',
                type=int,
                location='query',
                description='Ограничить количество результатов (по умолчанию все)',
                required=False,
                default=100
            ),
            OpenApiParameter(
                name='user_id',
                type=int,
                location='query',
                description='Фильтр по ID пользователя',
                required=False
            ),
            OpenApiParameter(
                name='stage_id',
                type=int,
                location='query',
                description='Фильтр по ID этапа',
                required=False
            ),
        ],
        responses={
            200: {
                'description': 'Список полученных призов',
                'content': {
                    'application/json': {
                        'examples': {
                            'success': {
                                'summary': 'Успешный ответ',
                                'value': {
                                    'prizes': [
                                        {
                                            'username': 'player1',
                                            'rid': 'RID123',
                                            'image': 'http://example.com/media/prize.jpg',
                                            'title': 'Супер-приз',
                                            'created_at': '2024-03-03T10:30:00Z'
                                        }
                                    ]
                                }
                            },
                            'empty': {
                                'summary': 'Пустой список',
                                'value': {
                                    'prizes': []
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    def get(self,request):
        prizes = UserStagePrizes.objects.order_by('received_at')

        serializer = UserStagePrizeSerializer(prizes, many=True, context={'request': request})


        return Response({
            'prizes': serializer.data
        })
