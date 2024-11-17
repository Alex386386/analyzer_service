from enum import Enum
from http import HTTPStatus

from fastapi import HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.crud_foundation import CRUDBase
from src.logger import logger


class Tags(Enum):
    reports = "Reports"
    sales = "Sales Data"


def get_redis_client(request: Request):
    if settings.test:
        return None
    return request.app.state.redis_client


def log_and_raise_error(message_log: str, message_error: str, status_code: HTTPStatus):
    """Логирование ошибки и возврат ошибки обратно в качестве ответа наз запрос."""
    logger.error(message_log)
    raise HTTPException(status_code=status_code, detail=message_error)


def check_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Функция проверки корректности поступающего токена."""
    if credentials:
        token = credentials.credentials
        if token != settings.access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid!"
            )
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлены учетные данные!",
        )


async def check_exists_and_get_or_return_error(
    db_id: any,
    crud: CRUDBase,
    method_name: str,
    error: str,
    status_code: HTTPStatus,
    session: AsyncSession,
):
    """
    Стандартная функция получения объекта по id или ключу из БД с вызовом указанного метода,
    а также с возвращением конкретной ошибки и указанного статус кода в случае отсутствия подобного объекта в БД.
    """
    method = getattr(crud, method_name, None)
    if method is None:
        log_and_raise_error(
            f"Метод {method_name} не найден в CRUD",
            "Invalid method",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    model_object = await method(db_id, session)
    if model_object is None:
        log_and_raise_error(
            f"Объект с id или name ({db_id}) не найден в БД",
            f"{error}",
            status_code,
        )
    logger.info(f"Объект с id или name ({db_id}) успешно получен из БД")
    return model_object
