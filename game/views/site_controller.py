from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.FAQ import FAQ
from game.models.rule_image import RuleImage
from game.serializers.FAQ_serializer import FAQSerializer
from game.serializers.rule_serializer import RulesSerializer


class SiteRules(APIView):
    permission_classes = [IsAuthenticated]


    @extend_schema(
        summary="Изображения правил",
        description="Возвращает список URL изображений с правилами игры, отсортированных по позиции.",
        tags=['Site'],
        responses={
            200: {
                'description': 'Список URL изображений правил',
                'content': {
                    'application/json': {
                        'examples': {
                            'success': {
                                'summary': 'Успешный ответ',
                                'value': {
                                    'rules': [
                                        'http://example.com/media/rules/rule1.jpg',
                                        'http://example.com/media/rules/rule2.jpg',
                                        'http://example.com/media/rules/rule3.jpg'
                                    ]
                                }
                            },
                            'empty': {
                                'summary': 'Пустой список',
                                'value': {
                                    'rules': []
                                }
                            }
                        }
                    }
                }
            },
            401: {
                'description': 'Не авторизован',
                'content': {
                    'application/json': {
                        'example': {'detail': 'Учетные данные не были предоставлены.'}
                    }
                }
            }
        }
    )
    def get(self,request):
        rules = RuleImage.objects.order_by('position')

        serializer = RulesSerializer(rules, many=True, context={'request': request})


        return Response({
           'rules': serializer.data
        })


class SiteFAQ(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Часто задаваемые вопросы",
        description="Возвращает список FAQ, отсортированных по позиции.",
        tags=['Site'],
        responses={
            200: {
                'description': 'Список FAQ',
                'content': {
                    'application/json': {
                        'examples': {
                            'success': {
                                'summary': 'Успешный ответ',
                                'value': {
                                    'faq': [
                                        {
                                            'question': 'Как начать играть?',
                                            'answer': 'Для начала игры нажмите кнопку "Старт" в главном меню.'
                                        },
                                        {
                                            'question': 'Как получить бонусы?',
                                            'answer': 'Бонусы можно получить за выполнение ежедневных заданий.'
                                        }
                                    ]
                                }
                            },
                            'empty': {
                                'summary': 'Пустой список',
                                'value': {
                                    'faq': []
                                }
                            }
                        }
                    }
                }
            },
            401: {
                'description': 'Не авторизован',
                'content': {
                    'application/json': {
                        'example': {'detail': 'Учетные данные не были предоставлены.'}
                    }
                }
            }
        }
    )
    def get(self, request):
        faq = FAQ.objects.order_by('position')

        serializer = FAQSerializer(faq, many=True, context={'request': request})

        return Response({
            'faq': serializer.data
        })