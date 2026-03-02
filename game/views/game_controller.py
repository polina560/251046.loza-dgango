# game/views/game_controller.py
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


class GameController(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, action=None):
        """Обработка POST запросов"""
        if action == 'start':
            return self.start(request)
        elif action == 'pause':
            return self.pause(request)
        elif action == 'abort':
            return self.abort(request)
        elif action == 'end':
            return self.end(request)
        else:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, action=None):
        """Обработка GET запросов"""
        if action == 'params':
            return self.params(request)
        else:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def start(self, request):
        """
        Начать новую игру.
        POST /api/game/start
        """
        user = request.user

        # Получаем платформу из запроса
        platform_value = request.data.get('platform', GamePlatform.SITE)

        # Преобразуем в соответствующий enum
        platform_map = {
            0: GamePlatform.SITE,
            1: GamePlatform.APPLICATION,
            2: GamePlatform.TELEGRAM,
        }
        platform = platform_map.get(platform_value, GamePlatform.SITE)

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

    def pause(self, request):
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

    def abort(self, request):
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

    def end(self, request):
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

    def params(self, request):
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