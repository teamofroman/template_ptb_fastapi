from http import HTTPStatus


class ApplicationError(Exception):
    """Общая ошибка приложения."""

    detail: str = 'Ошибочка... Мы ее найдем и исправим...'


class UnauthorizedError(ApplicationError):
    """Ошибка авторизации."""

    status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED
    detail = 'У Вас нет прав для просмотра запрошенной страницы.'
