from pathlib import Path
from typing import AnyStr
from urllib.parse import urljoin

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Класс настроек."""

    app_title: str = 'Test FastAPI TgBot Webhook APP'
    debug_mode: bool = False
    bot_token: str
    secret_key: str
    bot_webhook_mode: bool = False
    base_url: str = 'http://localhost/'

    class Config:
        """Класс конфигурации настроек."""

        env_file = BASE_DIR / 'infra/.env'
        extra = 'ignore'

    @property
    def webhook_url(self) -> AnyStr:
        """Возвращает URL для вебхук."""
        return urljoin(self.base_url, 'telegram/webhooks')


settings = Settings()
