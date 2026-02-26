# game/views.py (или api/views.py)

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models.user_game import GamePlatform, UserGameManager




class GameView(APIView):
    """
    Контроллер для игровых действий (начало, пауза, прерывание, завершение,
    а также получение игровых параметров).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, action):
        """
        Диспетчер для POST-запросов (start, pause, abort, end).
        """
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
        """
        GET-запрос для получения параметров игры.
        """
        if action == 'params':
            return self.params(request)
        else:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def start(self, request):
        """
        Начало новой игры.
        POST /game/start
        Параметры: platform (integer)
        """
        user = request.user
        platform_value = request.data.get('platform', GamePlatform.SITE)
        # Преобразуем число в строковый код платформы, если необходимо
        platform_map = {
            10: GamePlatform.SITE,
            20: GamePlatform.APPLICATION,
            # добавьте другие соответствия при необходимости
        }
        platform = platform_map.get(platform_value, GamePlatform.SITE)

        manager = UserGameManager(request)
        game_state = manager.start(user, platform)

        # Сериализуем профиль и состояние игры
        profile_serializer = ProfileSerializer(user)
        game_serializer = UserGameSerializer(game_state)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data
        })

    def pause(self, request):
        """
        Поставить игру на паузу / снять с паузы.
        POST /game/pause
        """
        user = request.user
        manager = UserGameManager(request)
        game_state = manager.pause(user)

        if not game_state:
            return Response(
                {'error': 'Нет активной игры'},
                status=status.HTTP_404_NOT_FOUND
            )

        profile_serializer = ProfileSerializer(user)
        game_serializer = UserGameSerializer(game_state)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data
        })

    def abort(self, request):
        """
        Прервать игру.
        POST /game/abort
        """
        user = request.user
        manager = UserGameManager(request)
        game_record = manager.abort(user)  # возвращает объект UserGames

        if not game_record:
            return Response(
                {'error': 'Нет активной игры'},
                status=status.HTTP_404_NOT_FOUND
            )

        profile_serializer = ProfileSerializer(user)
        game_serializer = UserGameSerializer(game_record)

        return Response({
            'profile': profile_serializer.data,
            'log': game_serializer.data
        })

    def end(self, request):
        """
        Завершить игру.
        POST /game/end
        Параметры: quest_completed (bool), damage_dealt (int), damage_taken (int)
        """
        user = request.user
        quest_completed = request.data.get('quest_completed', False)
        damage_dealt = int(request.data.get('damage_dealt', 0))
        damage_taken = int(request.data.get('damage_taken', 0))

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

            # Если квест действительно выполнен (проверяем is_quest и quest_completed)
            if game_record.is_quest and game_record.quest_completed:
                # Пытаемся списать попытку квеста
                if extra.complete_quest():
                    # Получаем награды из настроек игры
                    try:
                        money_reward = GameSetting.objects.get(name='quest_money_reward').value
                        glory_reward = GameSetting.objects.get(name='quest_glory_reward').value
                    except GameSetting.DoesNotExist:
                        money_reward = 0
                        glory_reward = 0

                    delta_money = int(money_reward)
                    delta_glory = int(glory_reward)

                    if delta_money > 0:
                        extra.add_money(delta_money)
                    if delta_glory > 0:
                        extra.add_glory(delta_glory)

            extra.save()
        except AttributeError:
            # UserExtra не существует – игнорируем
            pass

        profile_serializer = ProfileSerializer(user)
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
        GET /game/params
        """
        # Параметры игры из модели GameSetting
        settings_qs = GameSetting.objects.all()
        settings_dict = {s.name: s.value for s in settings_qs}
        # Если нужно, можно использовать сериализатор, который преобразует в список пар
        # Но для удобства вернём словарь (как в Laravel)
        params = settings_dict

        # Флаг демо-режима из настроек Django
        is_demo = getattr(settings, 'GAME_IS_DEMO', False)

        # Этапы
        stages = Stage.objects.all().order_by('start_at')
        stages_serializer = StageSerializer(stages, many=True)

        # Текущий этап (аналог скоупа current)
        current_stage = Stage.objects.filter(start_at__lte=timezone.now()).order_by('-start_at').first()
        current_stage_serializer = StageSerializer(current_stage) if current_stage else None

        # Кланы
        clans = Clan.objects.all()
        clans_serializer = ClanSerializer(clans, many=True)

        return Response({
            'params': params,  # или использовать GameSettingSerializer(settings_qs, many=True)
            'isDemo': is_demo,
            'stages': stages_serializer.data,
            'currentStage': current_stage_serializer.data if current_stage_serializer else None,
            'clans': clans_serializer.data,
        })