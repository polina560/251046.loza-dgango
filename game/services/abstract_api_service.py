# services/abstract_api_service.py
import logging
import requests
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from django.conf import settings


class AbstractApiService(ABC):
    """
    Абстрактный базовый класс для API сервисов.
    Аналог AbstractApiService в Laravel.
    """

    def __init__(self):
        self.base_url = self.get_base_url()
        self.default_headers = self.get_default_headers()
        self.timeout = getattr(settings, 'API_TIMEOUT', 30)
        self.logger = logging.getLogger(self.get_log_channel())

    @abstractmethod
    def get_base_url(self) -> str:
        """Возвращает базовый URL API"""
        pass

    def get_default_headers(self) -> Dict[str, str]:
        """Возвращает заголовки по умолчанию"""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def get_log_channel(self) -> str:
        """Возвращает название канала для логирования"""
        return 'api'

    def create_request_session(self) -> requests.Session:
        """
        Создаёт сессию для запросов.
        Аналог createBaseRequest() в Laravel.
        """
        session = requests.Session()
        session.headers.update(self.default_headers)
        return session

    def send_request(
            self,
            method: str,
            session: requests.Session,
            endpoint: str,
            data: Optional[Dict] = None,
            params: Optional[Dict] = None
    ) -> requests.Response:
        """
        Отправляет HTTP запрос.
        Аналог sendRequest() в Laravel.
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = session.request(
                method=method,
                url=url,
                json=data if method.lower() in ['post', 'put', 'patch'] else None,
                params=params,
                timeout=self.timeout
            )

            # Логируем запрос
            self.logger.debug(f"API Request: {method} {url} - Status: {response.status_code}")

            return response

        except requests.exceptions.Timeout:
            self.logger.error(f"API Timeout: {method} {url}")
            raise ConnectionError(f"Timeout connecting to {url}")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"API Connection Error: {method} {url} - {e}")
            raise ConnectionError(f"Failed to connect to {url}")
        except Exception as e:
            self.logger.error(f"API Unexpected Error: {method} {url} - {e}")
            raise
