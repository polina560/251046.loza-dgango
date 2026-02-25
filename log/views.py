# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.models import UserProfile
from account.serializers import ProfileSerializer
from .models import GamePlatform
from .serializers import UserGamesSerializer


class GameViewSet(viewsets.GenericViewSet):
    """
    ViewSet для игр пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserGamesSerializer

    @action(detail=False, methods=['post'], url_path='start')
    def start(self, request):
        """
        Начать новую игру
        POST /game/start/
        """
        user = request.user

        # Получаем платформу
        platform_value = request.data.get('platform', GamePlatform.SITE.value)

        try:
            platform_value = int(platform_value)
        except (ValueError, TypeError):
            platform_value = GamePlatform.SITE.value

        platform = None
        for choice in GamePlatform.values:
            if choice == str(platform_value) or choice == platform_value:
                platform = choice
                break

        if not platform:
            platform = GamePlatform.SITE

        # Начинаем игру
        game_state = request.game_manager.start(user, platform)

        # Получаем профиль
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = None

        # Сериализуем
        profile_data = ProfileSerializer(profile).data if profile else {}

        if isinstance(game_state, dict):
            game_data = {
                'user_id': game_state['user_id'],
                'started_at': game_state['started_at'],
                'status': game_state['status'],
                'platform': game_state['platform'],
                'is_quest': game_state['is_quest'],
            }
        else:
            game_data = UserGamesSerializer(game_state).data

        return Response({
            'profile': profile_data,
            'log': game_data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='pause')
    def pause(self, request):
        """
        Поставить игру на паузу / снять с паузы
        POST /game/pause/
        """
        user = request.user
        game_state = request.game_manager.pause(user)

        if not game_state:
            return Response(
                {'error': 'No active game'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'game_state': game_state
        })

    @action(detail=False, methods=['post'], url_path='abort')
    def abort(self, request):
        """
        Прервать игру
        POST /game/abort/
        """
        user = request.user
        game = request.game_manager.abort(user)

        if not game:
            return Response(
                {'error': 'No active game'},
                status=status.HTTP_400_BAD_REQUEST
            )

        game.save()

        return Response({
            'game': UserGamesSerializer(game).data
        })

    @action(detail=False, methods=['post'], url_path='end')
    def end(self, request):
        """
        Завершить игру
        POST /game/end/
        """
        user = request.user
        quest_completed = request.data.get('quest_completed', False)

        if isinstance(quest_completed, str):
            quest_completed = quest_completed.lower() == 'true'

        game = request.game_manager.end(user, quest_completed)

        if not game:
            return Response(
                {'error': 'No active game'},
                status=status.HTTP_400_BAD_REQUEST
            )

        game.save()

        return Response({
            'game': UserGamesSerializer(game).data
        })

    @action(detail=False, methods=['get'], url_path='state')
    def state(self, request):
        """
        Получить текущее состояние игры
        GET /game/state/
        """
        user = request.user
        state = request.game_manager._get_state_from_session(user.id)

        if not state:
            return Response(
                {'error': 'No active game'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'game_state': state
        })