from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from starlette import status

from backend import constants, models
from backend.middleware.auth import verify_access_token
from backend.services.user import UserService
from backend.utils.auth import get_user_from_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)], prefix="/user")


@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
    response_description="Пользователь успешно создан",
    response_model=models.UserGet,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def create_user(
    user: models.UserSignUp = Body(..., description="Тело запроса для создания пользователя"),
    requester_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.create_user(requester_id, user=user)



@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о текущем пользователе",
    response_description="Информация о текущем пользователе успешно получена",
    response_model=models.UserGetWithoutPassword,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_current_user(
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.get_user_by_id(user_id=user_id, guid=user_id)


@router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Полностью обновить информацию о текущем пользователе",
    response_description="Информация о текущем пользователе успешно обновлена",
    response_model=models.UserGetWithoutPassword,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def update_current_user(
    user: models.UserUpdate = Body(..., description="Тело запроса для обновления пользователя"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.change_user(user_id=user_id, guid=user_id, user=user)


@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Частично обновить информацию о текущем пользователе",
    response_description="Информация о текущем пользователе успешно обновлена",
    response_model=models.UserGetWithoutPassword,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def patch_current_user(
    user: models.UserPatch = Body(..., description="Тело запроса для обновления пользователя"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.change_user(user_id=user_id, guid=user_id, user=user)

@router.get(
    "/me/bookings",
    status_code=status.HTTP_200_OK,
    summary="Получить список забронированных услуг пользователя",
    response_description="Список забронированных услуг пользователя успешно получен",
    response_model=List[models.BookingGet],
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_user_bookings(
    limit: int = Query(default=10, description="Количество забронированных услуг", alias="limit"),
    offset: int = Query(default=0, description="Смещение", alias="offset"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.get_all_bookings_by_id(recipient_id=user_id, user_id=user_id, limit=limit, offset=offset)

@router.get(
    "/{id}/bookings",
    status_code=status.HTTP_200_OK,
    summary="Получить список забронированных услуг пользователя",
    response_description="Список забронированных услуг пользователя успешно получен",
    response_model=List[models.BookingGet],
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_user_bookings(
    limit: int = Query(default=10, description="Количество забронированных услуг", alias="limit"),
    offset: int = Query(default=0, description="Смещение", alias="offset"),
    user_id: UUID4 = Path(..., description="Идентификатор пользователя", alias="id"),
    recipient_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.get_all_bookings_by_id(recipient_id=recipient_id, user_id=user_id, limit=limit, offset=offset)

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Получить список пользователей",
    response_description="Список пользователей успешно получен",
    response_model=Dict[str, List[models.UserGetWithoutPassword]],
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_all_users(
    limit: int = Query(default=10, description="Количество пользователей", alias="limit"),
    offset: int = Query(default=0, description="Смещение", alias="offset"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> Dict[str, List[models.UserGetWithoutPassword]]:
    result = await user_service.get_all_users(user_id=user_id, limit=limit, offset=offset)
    return {"users": result}

@router.get(
    "/all/{role}",
    status_code=status.HTTP_200_OK,
    summary="Получить список пользователей с определенной ролью",
    response_description="Список пользователей успешно получен",
    response_model=Dict[str, List[models.UserGetWithoutPassword]],
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_all_users(
    limit: int = Query(default=10, description="Количество пользователей", alias="limit"),
    offset: int = Query(default=0, description="Смещение", alias="offset"),
    role: models.UserRole = Path(description="Роль пользователя", alias="role"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> Dict[str, List[models.UserGetWithoutPassword]]:
    result = await user_service.get_all_users_with_role(user_id=user_id, limit=limit, offset=offset, role=role)
    return {"users": result}

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя",
    response_description="Пользователь успешно получен",
    response_model=models.UserGetWithoutPassword,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_user_by_id(
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.get_user_by_id(user_id=user_id, guid=id_)


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя",
    response_description="Пользователь успешно обновлен",
    response_model=models.UserGetWithoutPassword,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def update_user_by_id(
    user: models.UserUpdate = Body(..., description="Тело запроса для обновления пользователя"),
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.change_user(user_id=user_id, guid=id_, user=user)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Частично обновить пользователя",
    response_description="Пользователь успешно обновлен",
    response_model=models.UserGetWithoutPassword,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def patch_user_by_id(
    user: models.UserUpdate = Body(..., description="Тело запроса для обновления пользователя"),
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> models.UserGet:
    return await user_service.change_user(user_id=user_id, guid=id_, user=user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
    response_description="Пользователь успешно удален",
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def delete_user_by_id(
    id_: UUID4 = Path(..., description="Идентификатор пользователя", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    user_service: UserService = Depends(),
) -> Response:
    await user_service.delete_user(user_id=user_id, guid=id_)
    return Response(status_code=204)
