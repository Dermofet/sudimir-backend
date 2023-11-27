import traceback
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from backend.logging import log
from pydantic import UUID4, BaseModel
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import config

class Message(BaseModel):
    id: Optional[UUID4] = None
    message: str

    def __hash__(self):
        return hash((self.id, self.message))


endpoint_message = {
    ("POST", "/auth/signin"): "Ошибка входа в систему",
    ("POST", "/auth/signup"): "Ошибка регистрации в системе",

    ("GET", "/user/me"): "Ошибка получения текущего пользователя",
    ("PUT", "/user/me"): "Ошибка изменения текущего пользователя",
    ("PATCH", "/user/me"): "Ошибка изменения текущего пользователя",

    ("GET", "/user/{id}"): "Ошибка получения пользователя",
    ("PUT", "/user/{id}"): "Ошибка изменения пользователя",
    ("PATCH", "/user/{id}"): "Ошибка изменения пользователя",
    ("DELETE", "/user/{id}"): "Ошибка удаления пользователя",

    ("POST", "/service"): "Ошибка создания услуги",
    ("GET", "/service/all"): "Ошибка получения списка услуг",
    ("GET", "/service/{id}"): "Ошибка получения информации о услуге",
    ("PUT", "/service/{id}"): "Ошибка изменения информации о услуге",
    ("PATCH", "/service/{id}"): "Ошибка изменения информации о услуге",
    ("DELETE", "/service/{id}"): "Ошибка удаления информации о услуге",
}


def get_endpoint_message(request: Request) -> Optional[str]:
    method, path = request.scope["method"], request.scope["path"]
    for path_parameter, value in request.scope["path_params"].items():
        path = path.replace(value, "{" + path_parameter + "}")
    return endpoint_message.get((method, path))


class ValidationUtils:
    @staticmethod
    def validate_type_error(error):
        field = error["loc"][-1]
        type_ = error["type"].split(".")[-1]
        return f'Поле "{field}" Имеет неверный тип данных. Укажите "{type_}"'

    @staticmethod
    def validate_const(error):
        field = error["loc"][-1]
        value = error["ctx"]["given"]
        allowed_values = error["ctx"]["permitted"]
        return (
            f'Поле "{field}" имеет некорректное значение, Вы указали  "{value}". Возможные значения: {allowed_values}'
        )

    @staticmethod
    def validate_invalid_discriminator(error):
        allowed_values = error["ctx"]["allowed_values"]
        discriminator_value = error["ctx"]["discriminator_key"]
        user_value = error["ctx"]["discriminator_value"]

        return (
            f'Поле "{discriminator_value}" является обязательным. Вы указали "{user_value}".'
            f"Возможные значения: {allowed_values}"
        )

    @staticmethod
    def validate_missing(error):
        field = error["loc"][-1]
        return f'Поле "{field}" является обязательным'


templates_function = {
    "missing": ValidationUtils.validate_missing,
    "const": ValidationUtils.validate_const,
    "": ValidationUtils.validate_type_error,
    "invalid_discriminator": ValidationUtils.validate_invalid_discriminator,
}


class ValidationHandler:
    @classmethod
    async def _send_to_sentry(cls, request: Request, error):
        if not settings.SENTRY_DISABLE_LOGGING:
            try:
                raise HTTPException(400, error)
            except HTTPException as e:
                sentry_sdk.set_tag("status_code", 400)
                sentry_sdk.capture_exception(e)

    @classmethod
    async def _build_final_error(cls, request: Request, errors: List[Message]):
        return {"message": get_endpoint_message(request), "errors": list(set(errors))}

    @classmethod
    async def _build_message(cls, type_: str, error: dict):
        try:
            if type_ in templates_function.keys():
                return templates_function[type_](error)
            else:
                return templates_function[""](error)
        except KeyError:
            return error["msg"]

    @classmethod
    async def validation_handler(cls, request: Request, exc):
        errors = []
        for error in exc.errors():
            type_ = error["type"].split(".")[-1]
            message = await cls._build_message(type_, error)
            errors.append(Message(message=message))

        error = await cls._build_final_error(request, errors)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(error))


async def logging_handler(request: Request, exc: HTTPException):
    log.warning(f"{request.client.host}:{request.client.port} | {request.method} {request.url.path} - {exc.status_code}")
    error = {"message": get_endpoint_message(request), "errors": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(error))


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, ValidationHandler.validation_handler)
    app.add_exception_handler(HTTPException, logging_handler)
