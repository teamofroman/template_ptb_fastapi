from telegram.ext import Application, ApplicationBuilder, CommandHandler

from bot.handlers.common import start
from core.settings import settings


def create_bot() -> Application:
    """Создаем приложение, обеспечивающее работу бота."""
    bot_instance = ApplicationBuilder().token(settings.bot_token).build()

    # TODO: Здесь цепляем хендлеры бота
    bot_instance.add_handler(CommandHandler('start', start))

    return bot_instance


async def start_bot() -> None:
    """Запускаем бота."""
    bot_instance = create_bot()
    await bot_instance.initialize()
    if settings.bot_webhook_mode:
        bot_instance.updater = None
        await bot_instance.bot.set_webhook(
            url=settings.webhook_url,
            secret_token=settings.secret_key,
        )
    else:
        await bot_instance.updater.start_polling()
    await bot_instance.start()

    return bot_instance
