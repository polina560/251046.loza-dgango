from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
import json
from enum import Enum
from django.utils import timezone


class GamePlatform(models.TextChoices):
    """Платформы для игры (аналог Enum в Laravel)"""
    SITE = 'site', _('Site')
    MOBILE = 'mobile', _('Mobile')
    TELEGRAM = 'telegram', _('Telegram')


class GameStatus(models.TextChoices):
    """Статусы игры (аналог Enum в Laravel)"""
    NEW = 'new', _('New')
    PAUSED = 'paused', _('Paused')
    COMPLETED = 'completed', _('Completed')
    ABORTED = 'aborted', _('Aborted')

# Create your models here.
class UserGames(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='games')

    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Started At'))
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Ended At'))
    paused_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Paused At'))
    pause_duration = models.IntegerField(null=True, verbose_name=_('Pause Duration'))
    quest_completed = models.BooleanField(null=True, verbose_name=_('Quests Completed'))
    status = models.SmallIntegerField(null=True, verbose_name=_('Status'))
    is_quest = models.BooleanField(default=False, verbose_name=_('Is Quest'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        indexes = [
            models.Index(fields=['started_at']),
            models.Index(fields=['started_at', 'user_id']),
        ]
        verbose_name = _('User Game')
        verbose_name_plural = _('User Games')


class UserGameManager:
    """
    Менеджер для работы с играми пользователя (аналог статических методов в Laravel)
    """

    def __init__(self, request):
        """
        Инициализация с request для доступа к сессии
        """
        self.request = request
        self.session = request.session

    @staticmethod
    def _get_session_key(user_id):
        """Получить ключ сессии для пользователя"""
        return f"user_game_{user_id}"

    def _get_state_from_session(self, user_id):
        """
        Получить состояние игры из сессии
        Аналог getStateFromSession в Laravel
        """
        session_key = self._get_session_key(user_id)
        state_json = self.session.get(session_key)

        if not state_json:
            return None

        try:
            return json.loads(state_json)
        except json.JSONDecodeError:
            return None

    def _save_state_to_session(self, user_id, state):
        """
        Сохранить состояние игры в сессию
        Аналог saveStateToSession в Laravel
        """
        session_key = self._get_session_key(user_id)
        self.session[session_key] = json.dumps(state, default=str)
        self.session.modified = True

    def _remove_state_from_session(self, user_id):
        """
        Удалить состояние игры из сессии
        Аналог removeStateFromSession в Laravel
        """
        session_key = self._get_session_key(user_id)
        if session_key in self.session:
            del self.session[session_key]
            self.session.modified = True

    def _create_game_state(self, user, platform):
        """
        Создать состояние игры
        Аналог createGameState в Laravel
        """
        # Получаем extra пользователя (если есть)
        try:
            user_extra = user.extra
            quests_count = (user_extra.quests or 0) + (user_extra.bonus_quests or 0)
        except:
            quests_count = 0

        return {
            'user_id': user.id,
            'started_at': timezone.now().isoformat(),
            'ended_at': None,
            'paused_at': None,
            'pause_duration': 0,
            'quest_completed': False,
            'status': GameStatus.NEW,
            'platform': platform,
            'is_quest': bool(quests_count),
        }

    def start(self, user, platform=GamePlatform.SITE):
        """
        Начать игру
        Аналог start в Laravel
        """
        # Прерываем предыдущую игру если есть
        aborted_game = self.abort(user)
        if aborted_game:
            aborted_game.save()

        # Создаем новое состояние
        new_state = self._create_game_state(user, platform)
        self._save_state_to_session(user.id, new_state)

        return new_state

    def pause(self, user):
        """
        Поставить игру на паузу / снять с паузы
        Аналог pause в Laravel
        """
        state = self._get_state_from_session(user.id)

        if not state or state['status'] not in [GameStatus.NEW, GameStatus.PAUSED]:
            return None

        if state['status'] == GameStatus.NEW:
            # Ставим на паузу
            state['status'] = GameStatus.PAUSED
            state['paused_at'] = timezone.now().isoformat()
        else:
            # Снимаем с паузы
            state['status'] = GameStatus.NEW
            if state['paused_at']:
                paused_at = timezone.datetime.fromisoformat(state['paused_at'])
                pause_seconds = (timezone.now() - paused_at).total_seconds()
                state['pause_duration'] += int(pause_seconds)
            state['paused_at'] = None

        self._save_state_to_session(user.id, state)

        return state

    def abort(self, user):
        """
        Прервать игру
        Аналог abort в Laravel
        """
        state = self._get_state_from_session(user.id)

        if not state or state['status'] not in [GameStatus.NEW, GameStatus.PAUSED]:
            return None

        # Создаем запись в БД
        game = UserGames(
            user_id=user.id,
            started_at=timezone.datetime.fromisoformat(state['started_at']),
            ended_at=timezone.now(),
            paused_at=timezone.datetime.fromisoformat(state['paused_at']) if state['paused_at'] else None,
            pause_duration=state['pause_duration'],
            quest_completed=False,
            status=GameStatus.ABORTED,
            platform=state['platform'],
            is_quest=state['is_quest']
        )

        # Удаляем из сессии
        self._remove_state_from_session(user.id)

        return game

    def end(self, user, quest_completed=False):
        """
        Завершить игру
        Аналог end в Laravel
        """
        state = self._get_state_from_session(user.id)

        if not state or state['status'] not in [GameStatus.NEW, GameStatus.PAUSED]:
            return None

        # Создаем запись в БД
        game = UserGames(
            user_id=user.id,
            started_at=timezone.datetime.fromisoformat(state['started_at']),
            ended_at=timezone.now(),
            paused_at=timezone.datetime.fromisoformat(state['paused_at']) if state['paused_at'] else None,
            pause_duration=state['pause_duration'],
            quest_completed=(state['is_quest'] and quest_completed),
            status=GameStatus.COMPLETED,
            platform=state['platform'],
            is_quest=state['is_quest']
        )

        # Удаляем из сессии
        self._remove_state_from_session(user.id)

        return game

class CouponModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='coupon',
    )
    number = models.CharField(verbose_name=_('Coupon Number'), max_length=20, null=True, blank=True)
    description = models.CharField(verbose_name=_('Description'), max_length=255, null=True, blank=True)
    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True)
    created = models.BooleanField(verbose_name=_('Created'), default=False)
    status = models.SmallIntegerField(null=True, verbose_name=_('Status'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))


    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
