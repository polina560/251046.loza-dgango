# game/views/game_controller.py
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings

from ..enum.game_plarform_choices import GamePlatform
from ..models.clan import Clan
from ..models.game_setting import GameSetting
from ..models.stage import Stage
from ..models.user_game import UserGameManager
from ..serializers.profile_serializer import ProfileSerializer
from ..serializers.stage_prize_serializer import StageSerializer
from ..serializers.user_game_serializer import UserGameSerializer
from ..serializers.clan_serializer import ClanSerializer

import logging

logger = logging.getLogger(__name__)


class GameStartView(APIView):

    permission_classes = [IsAuthenticated]


    @extend_schema(
        methods=['POST'],
        summary="Начать новую игру",
        description="Начало новой игровой сессии. Создает состояние игры в сессии пользователя.",
        tags=['Game'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'platform': {
                        'type': 'integer',
                        'enum': [0, 1],
                        'description': 'Платформа: 0 - сайт, 1 - приложение',
                        'default': 0
                    }
                }
            }
        },
        responses={
            200: {
                'description': 'Игра успешно начата',
                'content': {
                    'application/json': {
                        'example': {
                            'profile': {
                                'id': 'UID123',
                                'rid': 'RID123',
                                'username': 'player1',
                                'money': 1000,
                                'glory': 500,
                                'quests': 3
                            },
                            'log': {
                                'status': 0,
                                'quest_requirement': 100,
                                'quest_completed': False,
                                'is_quest': False
                            }
                        }
                    }
                }
            }
        }
    )

    def post(self, request):
        """
        Начать новую игру.
        POST /api/game/start
        """
        user = request.user

        # Получаем платформу из запроса
        platform = request.data.get('platform', GamePlatform.SITE)

        # Создаем менеджер и начинаем игру
        manager = UserGameManager(request)
        game_state = manager.start(user, platform)

        # Сериализуем ответ
        profile_serializer = ProfileSerializer(user, context={'request': request})
        game_serializer = UserGameSerializer(game_state)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data
        })

class GamePauseView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=['POST'],
        summary="Поставить игру на паузу / снять с паузы",
        description="Переключает состояние игры между паузой и активным режимом.",
        tags=['Game'],
        responses={
            200: {
                'description': 'Состояние игры изменено',
                'content': {
                    'application/json': {
                        'example': {
                            'profile': {},
                            'log': {
                                'status': 1,
                                'quest_requirement': 100,
                                'quest_completed': False,
                                'is_quest': False
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Нет активной игры',
                'content': {
                    'application/json': {
                        'example': {'error': 'Нет активной игры'}
                    }
                }
            }
        }
    )
    def post(self, request):
        """
        Поставить игру на паузу / снять с паузы.
        POST /api/game/pause
        """
        user = request.user
        manager = UserGameManager(request)
        game_state = manager.pause(user)

        if not game_state:
            return Response(
                {'error': 'Нет активной игры'},
                status=status.HTTP_404_NOT_FOUND
            )

        profile_serializer = ProfileSerializer(user, context={'request': request})
        game_serializer = UserGameSerializer(game_state)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data
        })

class GameAbortView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=['POST'],
        summary="Прервать игру",
        description="Прерывает текущую игровую сессию и сохраняет запись в истории.",
        tags=['Game'],
        responses={
            200: {
                'description': 'Игра прервана',
                'content': {
                    'application/json': {
                        'example': {
                            'profile': {},
                            'log': {
                                'status': 3,
                                'quest_requirement': 100,
                                'quest_completed': False,
                                'is_quest': False
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Нет активной игры',
                'content': {
                    'application/json': {
                        'example': {'error': 'Нет активной игры'}
                    }
                }
            }
        }
    )
    def post(self, request):
        """
        Прервать игру.
        POST /api/game/abort
        """
        user = request.user
        manager = UserGameManager(request)
        game_record = manager.abort(user)

        if not game_record:
            return Response(
                {'error': 'Нет активной игры'},
                status=status.HTTP_404_NOT_FOUND
            )

        profile_serializer = ProfileSerializer(user, context={'request': request})
        game_serializer = UserGameSerializer(game_record)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data
        })

class GameEndView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        methods=['POST'],
        summary="Завершить игру",
        description="Завершает текущую игровую сессию, начисляет награды и сохраняет запись в истории.",
        tags=['Game'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'quest_completed': {
                        'type': 'boolean',
                        'description': 'Был ли выполнен квест',
                        'default': False
                    },
                    'damage_dealt': {
                        'type': 'integer',
                        'description': 'Нанесенный урон',
                        'default': 0
                    },
                    'damage_taken': {
                        'type': 'integer',
                        'description': 'Полученный урон',
                        'default': 0
                    }
                }
            }
        },
        responses={
            200: {
                'description': 'Игра завершена',
                'content': {
                    'application/json': {
                        'example': {
                            'profile': {},
                            'log': {
                                'status': 2,
                                'quest_requirement': 100,
                                'quest_completed': True,
                                'is_quest': True
                            },
                            'deltaMoney': 50,
                            'deltaGlory': 10
                        }
                    }
                }
            },
            404: {
                'description': 'Нет активной игры',
                'content': {
                    'application/json': {
                        'example': {'error': 'Нет активной игры'}
                    }
                }
            }
        }
    )
    def post(self, request):
        """
        Завершить игру.
        POST /api/game/end
        """
        user = request.user

        # Получаем параметры завершения
        quest_completed = request.data.get('quest_completed', False)
        damage_dealt = int(request.data.get('damage_dealt', 0))
        damage_taken = int(request.data.get('damage_taken', 0))

        # Завершаем игру
        manager = UserGameManager(request)
        game_record = manager.end(user, quest_completed)

        if not game_record:
            return Response(
                {'error': 'Нет активной игры'},
                status=status.HTTP_404_NOT_FOUND
            )

        delta_money = 0
        delta_glory = 0

        # Обновляем статистику в UserExtra
        try:
            extra = user.extra
            extra.damage_dealt += damage_dealt
            extra.damage_taken += damage_taken

            # Если квест выполнен
            if game_record.is_quest and game_record.quest_completed:
                if extra.complete_quest():
                    # Получаем награды из настроек
                    try:
                        money_reward = GameSetting.objects.get(name='quest_money_reward').value
                        glory_reward = GameSetting.objects.get(name='quest_glory_reward').value
                    except GameSetting.DoesNotExist:
                        money_reward = getattr(settings, 'QUEST_MONEY_REWARD', 0)
                        glory_reward = getattr(settings, 'QUEST_GLORY_REWARD', 0)

                    delta_money = int(money_reward)
                    delta_glory = int(glory_reward)

                    if delta_money > 0:
                        extra.add_money(delta_money)
                    if delta_glory > 0:
                        extra.add_glory(delta_glory)

            extra.save()
        except AttributeError:
            logger.warning(f"User {user.id} has no extra data")

        profile_serializer = ProfileSerializer(user, context={'request': request})
        game_serializer = UserGameSerializer(game_record)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data,
            'deltaMoney': delta_money,
            'deltaGlory': delta_glory,
        })

class GameParamsView(APIView):

    permission_classes = [IsAuthenticated]
    @extend_schema(
        methods=['GET'],
        summary="Получить игровые параметры",
        description="Возвращает настройки игры, этапы, кланы и другую информацию.",
        tags=['Game'],
        responses={
            200: {
                'description': 'Параметры игры',
                'content': {
                    'application/json': {
                        'example': {
                            'params': {
                                'base_quests': '3',
                                'quest_cooldown': '3600'
                            },
                            'isDemo': False,
                            'stages': [],
                            'currentStage': None,
                            'clans': []
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        """
        Получить игровые параметры.
        GET /api/game/params
        """
        # Параметры игры
        settings_qs = GameSetting.objects.all()
        params = {s.name: s.value for s in settings_qs}

        # Демо-режим
        is_demo = getattr(settings, 'GAME_IS_DEMO', False)

        # Этапы
        stages = Stage.objects.all().order_by('start_at')
        stages_serializer = StageSerializer(stages, many=True, context={'request': request})

        # Текущий этап
        current_stage = Stage.current()
        current_stage_serializer = StageSerializer(
            current_stage, context={'request': request}
        ) if current_stage else None

        # Кланы
        clans = Clan.objects.all()
        clans_serializer = ClanSerializer(clans, many=True, context={'request': request})

        return Response({
            'params': params,
            'isDemo': is_demo,
            'stages': stages_serializer.data,
            'currentStage': current_stage_serializer.data if current_stage_serializer else None,
            'clans': clans_serializer.data,
        })