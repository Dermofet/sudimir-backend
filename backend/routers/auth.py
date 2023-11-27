from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from starlette import status

from backend import constants, models
from backend.services.auth import AuthService

router = APIRouter(prefix="/auth")


@router.post(
    "/signup",
    status_code=status.HTTP_200_OK,
    summary="Зарегистрировать нового пользователя",
    response_description="Регистрация прошла успешно",
    response_model=models.Token,
    responses={
        400: models.errors.BAD_REQUEST,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def signup(
    user: models.UserSignUp = Body(..., description="Тело запроса для создания пользователя"),
    auth_service: AuthService = Depends(),
) -> models.UserGet:
    return await auth_service.signup(user=user)


@router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
    summary="Вход пользователя в систему",
    response_description="Вход прошел успешно",
    response_model=models.Token,
    responses={
        400: models.errors.BAD_REQUEST,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def signup(
    user: models.UserSignIn = Body(..., description="Тело запроса для создания пользователя"),
    auth_service: AuthService = Depends(),
) -> models.UserGet:
    return await auth_service.signin(user=user)


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя без пароля",
    response_description="Пользователь успешно получен",
    response_model=models.UserGet,
    response_model_exclude={"password"},
    responses={
        400: models.errors.BAD_REQUEST,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def forgot_password(
    user: models.UserForgotPassword = Body(..., description="Тело запроса для получения пользователя без пароля"),
    auth_service: AuthService = Depends(),
) -> models.UserGet:
    return await auth_service.forgot_password(user=user)


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Смена пароля пользователя",
    response_description="Смена пароля прошла успешно",
    response_model=models.Token,
    responses={
        400: models.errors.BAD_REQUEST,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def change_password(
    user: models.UserChangePassword = Body(..., description="Тело запроса для смены пароля пользователя"),
    auth_service: AuthService = Depends(),
) -> models.UserGet:
    return await auth_service.change_password(user=user)