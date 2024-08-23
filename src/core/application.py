from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import webhook_router
from bot.bot_main import start_bot
from core.exception_handlers import (
    application_error_handler,
    internal_exception_handler,
)
from core.exeptions import ApplicationError
from core.settings import settings


def create_app() -> FastAPI:
    """Создаем основное приложения для FastAPI."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> None:
        """Обрабатываем жизненный цикл FastAPI."""
        # Запуск приложения
        bot_instance = await start_bot()
        app.state.bot_instance = bot_instance
        yield
        # Остановка приложения
        if not settings.bot_webhook_mode:
            await bot_instance.updater.stop()
        await bot_instance.stop()
        await bot_instance.shutdown()

    app = FastAPI(
        debug=settings.debug_mode,
        title=settings.app_title,
        lifespan=lifespan,
    )

    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # TODO: Здесь добавляем роутеры FastAPI
    app.include_router(webhook_router)

    # TODO: Здесь добавляем обработчики ошибок
    app.add_exception_handler(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        internal_exception_handler,
    )
    app.add_exception_handler(ApplicationError, application_error_handler)

    return app
