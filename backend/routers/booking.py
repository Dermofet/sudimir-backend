from typing import Dict, List

from fastapi import APIRouter, Body, Depends, Path, Query
from pydantic import UUID4
from starlette import status

from backend import constants, models
from backend.middleware.auth import verify_access_token
from backend.services.booking import BookingService
from backend.utils.auth import get_user_from_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)], prefix="/booking")


@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    summary="Создать бронь",
    response_description="Бронь успешно создана",
    response_model=models.BookingGet,
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
async def create_booking(
    booking: models.BookingCreate = Body(..., description="Тело брони"),
    requester_id: UUID4 = Depends(get_user_from_access_token),
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.create_booking(requester_id=requester_id, booking=booking)


@router.get(
    "/id/{id}",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о брони",
    response_description="Информация о брони успешно получена",
    response_model=models.BookingGet,
    responses={
        400: models.errors.BAD_REQUEST,
        401: models.errors.UNAUTHORIZED,
        403: models.errors.FORBIDDEN,
        404: models.errors.NOT_FOUND,
        422: models.errors.UNPROCESSABLE_ENTITY,
        429: models.errors.TOO_MANY_REQUESTS,
        500: models.errors.INTERNAL_SERVER_ERROR,
        503: models.errors.SERVICE_UNAVAILABLE,
    },
)
async def get_booking(
    id_: UUID4 = Path(..., description="Идентификатор брони", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.get_booking_by_id(user_id=user_id, booking_id=id_)

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о брони",
    response_description="Информация о брони успешно получена",
    response_model=Dict[str, List[models.BookingGet]],
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
async def get_all_bookings(
    limit: int = Query(constants.MAX_LIMIT, ge=1, le=constants.MAX_LIMIT, description="Ограничение на количество броней"),
    offset: int = Query(0, ge=0, le=constants.MAX_OFFSET, description="Смещение"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    booking_service: BookingService = Depends(),
) -> Dict[str, List[models.BookingGet]]:
    result = await booking_service.get_all_bookings(user_id=user_id, limit=limit, offset=offset)
    return {"bookings": result}

@router.put(
    "/{id}/status",
    status_code=status.HTTP_200_OK,
    summary="Изменить бронь",
    response_description="Бронь успешно изменена",
    response_model=models.BookingGet,
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
async def change_booking_status(
    id_: UUID4 = Path(..., description="Идентификатор брони", alias="id"),
    status: models.BookingStatusUpdate = Body(..., description="Тело запроса для изменения брони"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.change_booking_status(user_id=user_id, booking_id=id_, status=status)


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Изменить бронь",
    response_description="Бронь успешно изменена",
    response_model=models.BookingGet,
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
async def change_booking(
    id_: UUID4 = Path(..., description="Идентификатор брони", alias="id"),
    booking: models.BookingUpdate = Body(..., description="Тело запроса для изменения брони"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.change_booking(user_id=user_id, booking_id=id_, booking=booking)


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить бронь",
    response_description="Бронь успешно удалена",
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
async def delete_booking(
    booking_id: UUID4 = Path(..., description="Идентификатор брони", alias="id"),
    user_id: UUID4 = Depends(get_user_from_access_token),
    booking_service: BookingService = Depends(),
):
    return await booking_service.delete_booking(user_id=user_id, booking_id=booking_id)