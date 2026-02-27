# services/bristol_api.py
import base64
import logging
from typing import Optional, Dict, Any, List
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import requests

from .abstract_api_service import AbstractApiService


class BristolApi(AbstractApiService):
    """
    Сервис для работы с Bristol API.
    Аналог BristolApi в Laravel.
    """

    def __init__(self):
        # Получаем настройки из django.conf.settings
        self.api_url = getattr(settings, 'BRISTOL_API_URL', None)
        self.login = getattr(settings, 'BRISTOL_API_LOGIN', None)
        self.password = getattr(settings, 'BRISTOL_API_PASSWORD', None)
        self.log_channel = getattr(settings, 'BRISTOL_API_LOG_CHANNEL', 'bristol_api')

        # Проверяем наличие обязательных настроек
        if not all([self.api_url, self.login, self.password]):
            raise ImproperlyConfigured(
                'Bristol API credentials are not set. '
                'Please define BRISTOL_API_URL, BRISTOL_API_LOGIN, and BRISTOL_API_PASSWORD in settings.'
            )

        # Инициализируем родительский класс
        super().__init__()

        # Создаём логгер
        self.logger = logging.getLogger(self.log_channel)

    def get_base_url(self) -> str:
        """Возвращает базовый URL API"""
        return self.api_url

    def get_default_headers(self) -> Dict[str, str]:
        """Возвращает заголовки по умолчанию с Basic Auth"""
        headers = super().get_default_headers()

        # Добавляем Basic Authentication
        auth_string = f"{self.login}:{self.password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        headers['Authorization'] = f'Basic {encoded_auth}'

        return headers

    def get_log_channel(self) -> str:
        """Возвращает название канала для логирования"""
        return self.log_channel

    def issue_coupon(self, user_uid: str) -> Dict[str, Any] | int:
        """
        Выдаёт купон пользователю.

        Args:
            user_uid: внешний ID пользователя

        Returns:
            Dict с данными купона или int (код ошибки)

        Raises:
            ConnectionError: при ошибках соединения
        """
        session = self.create_request_session()

        try:
            response = self.send_request(
                method='post',
                session=session,
                endpoint='/loyalty/api/v1/coupons/',
                data={'user_external_id': user_uid}
            )

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'coupon' in data:
                    coupon = data['coupon']
                    # Преобразуем в нужный формат
                    return {
                        'number': coupon.get('number'),
                        'description': coupon.get('description'),
                        'image_url': coupon.get('image_url'),
                        'created': coupon.get('created', False),
                    }

            # Возвращаем код ошибки
            self.logger.warning(
                f"Bristol API returned non-200 status: {response.status_code} - {response.text}"
            )
            return response.status_code

        except ConnectionError as e:
            self.logger.error(f"Connection error in issue_coupon: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in issue_coupon: {e}")
            return 500

    def winners(self, top_users: List[Dict[str, Any]]) -> bool:
        """
        Отправляет список победителей.

        Args:
            top_users: список словарей с данными победителей в формате:
                [
                    {
                        'user_external_id': str,
                        'place': int,
                        'season': str,
                        'rating': int
                    },
                    ...
                ]

        Returns:
            bool: True если успешно

        Raises:
            ConnectionError: при ошибках соединения
        """
        session = self.create_request_session()

        try:
            response = self.send_request(
                method='post',
                session=session,
                endpoint='/loyalty/api/v1/winners/',
                data=top_users
            )

            if response.status_code == 200:
                self.logger.info(f"Successfully sent {len(top_users)} winners to Bristol API")
                return True
            else:
                self.logger.error(
                    f"Failed to send winners. Status: {response.status_code} - {response.text}"
                )
                return False

        except ConnectionError as e:
            self.logger.error(f"Connection error in winners: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in winners: {e}")
            return False

    def winners_from_ratings(self, ratings_collection) -> bool:
        """
        Отправляет список победителей из коллекции UserRating.
        Аналог метода в Laravel, принимающего Collection<UserRating>.

        Args:
            ratings_collection: QuerySet или список UserRating объектов

        Returns:
            bool: True если успешно
        """
        # Преобразуем QuerySet в список словарей
        top_users = []

        for idx, rating in enumerate(ratings_collection):
            # Получаем user_id из связанного пользователя
            user_uid = None
            if hasattr(rating.user, 'profile'):
                user_uid = rating.user.profile.uid
            elif hasattr(rating, 'user_id'):
                # Загружаем пользователя при необходимости
                user_uid = rating.user.profile.uid if hasattr(rating.user, 'profile') else None

            top_users.append({
                'user_external_id': user_uid,
                'place': idx + 1,
                'season': rating.stage.title if rating.stage else None,
                'rating': rating.glory,
            })

        return self.winners(top_users)


# Создаём экземпляр сервиса для удобного импорта
bristol_api = BristolApi()