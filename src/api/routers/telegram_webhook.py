from fastapi import APIRouter, Request
from telegram import Update

from core.exeptions import UnauthorizedError
from core.settings import settings

router = APIRouter(prefix='/telegram', tags=['Telegram'])

if settings.bot_webhook_mode:

    @router.post(
        '/webhooks',
        summary='Получение обновлений Telegram',
        response_description='Обновления получены',
    )
    async def telegram_bot_updates(request: Request) -> dict:
        """Обработка уведомлений от Telegram."""
        secret_token = request.headers.get(
            'X-Telegram-Bot-Api-Secret-Token',
            '',
        )
        if secret_token != settings.secret_key:
            raise UnauthorizedError

        bot_instance = request.app.state.bot_instance
        request_data = await request.json()
        await bot_instance.update_queue.put(
            Update.de_json(data=request_data, bot=bot_instance.bot),
        )

        return request_data
