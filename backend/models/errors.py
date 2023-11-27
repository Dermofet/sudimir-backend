from typing import Any, List, Literal, Optional

from pydantic import Field

from backend.models.utils import ApiModel


class BaseError(ApiModel):
    type: Optional[str] = Field(None)
    message: str

    def __hash__(self):
        return hash(self.type)


class ValidationError(BaseError):
    type: Literal['fieldValidationError']
    value: Any
    field: Optional[str]

    def __hash__(self):
        return hash((self.type, self.value, self.field))


class ErrorMessage(ApiModel):
    message: str
    errors: List[BaseError]


BAD_REQUEST = {"model": ErrorMessage, "description": "Запрос содержит ошибки и не может быть обработан"}
UNAUTHORIZED = {"model": ErrorMessage, "description": "Ошибка авторизации"}
FORBIDDEN = {"model": ErrorMessage, "description": "Отказано в доступе"}
NOT_FOUND = {"model": ErrorMessage, "description": "Не найдено ни одного объекта с заданными параметрами"}
CONFLICT = {"model": ErrorMessage, "description": "Объект уже существует или содержит конфликтные изменения"}
UNPROCESSABLE_ENTITY = {
    "model": ErrorMessage,
    "description": "Запрос принят в обработку, но проверка верности параметров запроса неуспешна",
}
TOO_MANY_REQUESTS = {"model": ErrorMessage, "description": "Отказано в обработке из-за большого количества обращений"}
INTERNAL_SERVER_ERROR = {
    "model": ErrorMessage,
    "description": "Отказано в обработке из-за неизвестной ошибки на сервере",
}
SERVICE_UNAVAILABLE = {"model": ErrorMessage, "description": "Отказано в обработке из-за перегрузки сервера"}
BAD_GATEWAY = {"model": ErrorMessage, "description": "Получен неправильный ответ сервера"}
