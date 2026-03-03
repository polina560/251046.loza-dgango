from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.sale import Sale
from game.serializers.sale_serializer import SaleSerializer


class SaleView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Список акций",
        description="Возвращает список всех акций, отсортированных по позиции.",
        tags=['Sales'],
        parameters=[
            OpenApiParameter(
                name='limit',
                type=int,
                location='query',
                description='Ограничить количество результатов (по умолчанию все)',
                required=False
            ),
            OpenApiParameter(
                name='position',
                type=int,
                location='query',
                description='Фильтр по позиции',
                required=False
            ),
        ],
        responses={
            200: {
                'description': 'Список акций',
                'content': {
                    'application/json': {
                        'examples': {
                            'success': {
                                'summary': 'Успешный ответ',
                                'value': [
                                    {
                                        'title': 'Летняя распродажа',
                                        'images': [
                                            'http://example.com/media/sale1.jpg',
                                            'http://example.com/media/sale2.jpg'
                                        ]
                                    },
                                    {
                                        'title': 'Зимняя распродажа',
                                        'images': [
                                            'http://example.com/media/sale3.jpg'
                                        ]
                                    }
                                ]
                            },
                            'empty': {
                                'summary': 'Пустой список',
                                'value': []
                            }
                        }
                    }
                }
            }
        }
    )
    def get(self,request):
        sales = Sale.objects.order_by('position')

        serializer = SaleSerializer(sales, many=True, context={'request': request})


        return Response({
            serializer.data
        })
