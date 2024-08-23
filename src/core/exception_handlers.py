from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

DEFAULT_ERROR_MESSAGES = 'Что-то сломалось, но мы это уже чиним.'


async def internal_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Обработка внутренней ошибки сервера (500)."""
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={'detail': DEFAULT_ERROR_MESSAGES},
    )


async def application_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Обработка ошибки приложения."""
    status_code = getattr(exc, 'status_code', None)
    error_message = getattr(exc, 'detail', None)

    if status_code is None or error_message is None:
        return await internal_exception_handler(request, exc)

    return JSONResponse(
        status_code=status_code,
        content={'detail': error_message},
    )
