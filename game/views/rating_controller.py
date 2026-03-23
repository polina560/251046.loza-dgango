# game/views/rating_controller.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from game.models.clan_rating import ClanRating
from game.models.stage import Stage
from game.models.user_rating import UserRating
from game.serializers.user_rating_serializer import UserRatingSerializer

import logging

logger = logging.getLogger(__name__)


class RatingIndexView(APIView):
    """
    Получение текущего рейтинга пользователей.
    GET /api/rating/index
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Текущий рейтинг пользователей",
        description="Получение пагинированного списка пользователей в рейтинге",
        tags=['Rating'],
        parameters=[
            OpenApiParameter(
                name='stage_id',
                description='ID этапа (по умолчанию текущий)',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='clan_id',
                description='ID клана для фильтрации по клану',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='page',
                description='Номер страницы',
                required=False,
                type=int,
                default=1
            ),
            OpenApiParameter(
                name='per_page',
                description='Элементов на странице (макс. 30)',
                required=False,
                type=int,
                default=20
            ),
        ],
        responses={
            200: {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'example': {
                            'rating': [
                                {
                                    'position': 1,
                                    'clan_id': 1,
                                    'username': 'player1',
                                    'glory': 1500
                                }
                            ],
                            '_meta': {
                                'page': 1,
                                'pageCount': 10,
                                'pageSize': 20,
                                'totalCount': 200
                            }
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        # Получаем параметры запроса
        try:
            stage_id = request.query_params.get('stage_id')
            if stage_id:
                stage_id = int(stage_id)
            else:
                stage_id = Stage.cached_current_id()
        except (ValueError, TypeError):
            return Response(
                {'error': 'Некорректный ID этапа'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            clan_id = request.query_params.get('clan_id')
            clan_id = int(clan_id) if clan_id else None
        except ValueError:
            clan_id = None

        try:
            page = int(request.query_params.get('page', 1))
        except ValueError:
            page = 1

        try:
            per_page = int(request.query_params.get('per_page', 20))
            per_page = min(per_page, 30)  # Максимум 30 элементов
        except ValueError:
            per_page = 20

        # Получаем базовый queryset
        if clan_id:
            ratings_qs = UserRating.objects.by_clan(stage_id, clan_id)
        else:
            ratings_qs = UserRating.objects.global_rating(stage_id)

        ratings_qs = ratings_qs.select_related('user', 'clan')
        ratings_qs = ratings_qs.order_by('-glory', 'glory_time')

        paginator = Paginator(ratings_qs, per_page)

        try:
            current_page = paginator.page(page)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        # Вычисляем начальную позицию
        start_index = (current_page.number - 1) * per_page + 1

        # Формируем результат с позициями
        rating_data = []
        for idx, rating in enumerate(current_page.object_list, start=start_index):
            serializer = UserRatingSerializer(
                rating,
                context={'position': idx, 'request': request}
            )
            rating_data.append(serializer.data)

        return Response({
            'rating': rating_data,
            '_meta': {
                'page': current_page.number,
                'pageCount': paginator.num_pages,
                'pageSize': per_page,
                'totalCount': paginator.count,
            }
        })


class RatingClanView(APIView):
    """
    Получение текущего рейтинга кланов.
    GET /api/rating/clan
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Рейтинг кланов",
        description="Получение списка кланов в рейтинге",
        tags=['Rating'],
        parameters=[
            OpenApiParameter(
                name='stage_id',
                description='ID этапа (по умолчанию текущий)',
                required=False,
                type=int
            ),
        ],
        responses={
            200: {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'example': {
                            'clans': [
                                {
                                    'id': 1,
                                    'glory': 5000
                                }
                            ]
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        # Получаем параметры запроса
        try:
            stage_id = request.query_params.get('stage_id')
            if stage_id:
                stage_id = int(stage_id)
            else:
                stage_id = Stage.cached_current_id()
        except (ValueError, TypeError):
            return Response(
                {'error': 'Некорректный ID этапа'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем рейтинг кланов
        clan_ratings = ClanRating.objects.filter(
            stage_id=stage_id
        ).order_by('-total_glory').select_related('clan')

        # Формируем результат
        clans_data = [
            {
                'id': rating.clan_id,
                'glory': rating.total_glory
            }
            for rating in clan_ratings
        ]

        return Response({
            'clans': clans_data
        })


class RatingUserView(APIView):
    """
    Получение текущего рейтинга конкретного пользователя.
    GET /api/rating/user
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Рейтинг текущего пользователя",
        description="Получение позиции текущего пользователя в рейтинге",
        tags=['Rating'],
        parameters=[
            OpenApiParameter(
                name='stage_id',
                description='ID этапа (по умолчанию текущий)',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='clan_id',
                description='ID клана для рейтинга внутри клана',
                required=False,
                type=int
            ),
        ],
        responses={
            200: {
                'description': 'OK',
                'content': {
                    'application/json': {
                        'example': {
                            'user': {
                                'position': 15,
                                'clan_id': 1,
                                'username': 'player1',
                                'glory': 1200
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Пользователь не найден в рейтинге',
                'content': {
                    'application/json': {
                        'example': {'error': 'Вас нет в рейтинге'}
                    }
                }
            }
        }
    )
    def get(self, request):
        user = request.user

        # Получаем параметры запроса
        try:
            stage_id = request.query_params.get('stage_id')
            if stage_id:
                stage_id = int(stage_id)
            else:
                stage_id = Stage.cached_current_id()
        except (ValueError, TypeError):
            return Response(
                {'error': 'Некорректный ID этапа'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            clan_id = request.query_params.get('clan_id')
            clan_id = int(clan_id) if clan_id else None
        except ValueError:
            clan_id = None

        # Ищем рейтинг пользователя
        query = UserRating.objects.filter(
            user=user,
            stage_id=stage_id
        )

        if clan_id:
            query = query.filter(clan_id=clan_id)

        user_rating = query.first()

        if not user_rating:
            return Response(
                {'error': 'Вас нет в рейтинге'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Вычисляем позицию
        if clan_id:
            position = self._get_user_position_in_clan(user_rating, stage_id, clan_id)
        else:
            position = self._get_user_global_position(user_rating, stage_id)

        # Сериализуем результат
        serializer = UserRatingSerializer(
            user_rating,
            context={'position': position, 'request': request}
        )

        return Response({
            'user': serializer.data
        })

    def _get_user_global_position(self, user_rating, stage_id):
        """
        Получить позицию пользователя в глобальном рейтинге.
        """
        # Считаем количество пользователей с большей славой
        # или с такой же славой, но меньшим временем
        count = UserRating.objects.global_rating(stage_id).filter(
            Q(glory__gt=user_rating.glory) |
            Q(glory=user_rating.glory, glory_time__lt=user_rating.glory_time)
        ).count()

        return count + 1

    def _get_user_position_in_clan(self, user_rating, stage_id, clan_id):
        """
        Получить позицию пользователя в рейтинге клана.
        """
        count = UserRating.objects.by_clan(stage_id, clan_id).filter(
            Q(glory__gt=user_rating.glory) |
            Q(glory=user_rating.glory, glory_time__lt=user_rating.glory_time)
        ).count()

        return count + 1


# Объединенный контроллер (опционально)
class RatingController(APIView):
    """
    Общий контроллер для рейтингов.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == 'index':
            return RatingIndexView().get(request)
        elif action == 'clan':
            return RatingClanView().get(request)
        elif action == 'user':
            return RatingUserView().get(request)
        else:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )