from typing import List, Dict

from fastapi import APIRouter, Body, Depends, Path, Query
from pydantic import UUID4
from starlette import status

from backend import models
from backend.middleware.auth import verify_access_token
from backend.services.service import ServiceService
from backend.utils.auth import get_user_from_access_token

router_with_token = APIRouter(dependencies=[Depends(verify_access_token)], prefix="/service")
router_without_token = APIRouter(prefix="/service")


@router_with_token.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    summary="Получить информацию о услуге",
    response_description="Информация о услуге успешно получена",
    response_model=models.ServiceGet,
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
async def create_service(
    service: models.ServiceCreate = Body(..., description="Тело услуги"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    service_service: ServiceService = Depends(),
) -> models.UserGet:
    return await service_service.create_service(user_id=user_id, service=service)


@router_without_token.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Получить список услуг",
    response_description="Список услуг успешно получен",
    response_model=Dict[str, List[models.ServiceGet]],
    responses={
        400: models.errors.BAD_REQUEST,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_service_all(
    limit: int = Query(default=10, description="Количество услуг", alias="limit"),
    offset: int = Query(default=0, description="Смещение", alias="offset"),
    service_service: ServiceService = Depends(),
) -> Dict[str, List[models.ServiceGet]]:
    result = await service_service.get_all(limit=limit, offset=offset)
    return {"services": result}


@router_without_token.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о услуге",
    response_description="Информация о услуге успешно получена",
    response_model=models.ServiceGet,
    responses={
        400: models.errors.BAD_REQUEST,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_service_by_id(
    id_: UUID4 = Path(..., description="Идентификатор услуги", alias="id"),
    service_service: ServiceService = Depends(),
) -> models.ServiceGet:
    return await service_service.get_service_by_id(service_id=id_)



@router_with_token.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Изменить услугу",
    response_description="Услуга успешно изменена",
    response_model=models.ServiceGet,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def change_user_by_id(
    id_: UUID4 = Path(..., description="Идентификатор услуги", alias="id"),
    service: models.ServiceUpdate = Body(..., description="Тело запроса для получения услуги"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    service_service: ServiceService = Depends(),
) -> models.ServiceGet:
    return await service_service.change_service(user_id=user_id, service_id=id_, service=service)


@router_with_token.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Частично измененить услугу",
    response_description="Услуга успешно изменена",
    response_model=models.ServiceGet,
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
async def patch_service_by_id(
    id_: UUID4 = Path(..., description="Идентификатор услуги", alias="id"),
    service: models.ServicePatch = Body(..., description="Тело запроса для получения услуги"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    service_service: ServiceService = Depends(),
) -> models.ServiceGet:
    return await service_service.change_service(user_id=user_id, service_id=id_, service=service)


@router_with_token.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить услугу",
    response_description="Услуга успешно удалена",
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
async def delete_service_by_id(
    service_id: UUID4 = Path(..., description="Идентификатор услуги", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    service_service: ServiceService = Depends(),
):
    return await service_service.delete_service(user_id=user_id, service_id=service_id)
