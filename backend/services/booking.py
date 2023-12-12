import datetime
from typing import List, Tuple, Union

from fastapi import Depends, HTTPException, status
from backend.logging import log
from pydantic import UUID4

from backend import models
from backend.database.facade import DBFacadeInterface, get_db_facade
from backend.utils.user import check_user_existence_and_access


class BookingService:
    def __init__(self, db_facade: DBFacadeInterface = Depends(get_db_facade)):
        self._db_facade = db_facade

    async def create_booking(self, requester_id: UUID4, booking: models.BookingCreate) -> models.BookingGet:
        """Создать бронь"""

        log.debug(f"Пользователь {requester_id}: запрос на создание брони")

        requester = await self._db_facade.get_user_by_id(guid=requester_id)
        await check_user_existence_and_access(user=requester, roles=(models.UserRole.WORKER,
                                                                models.UserRole.ADMIN))
        
        user = await self._db_facade.get_user_by_phone(phone=booking.phone)
        if not user:
            new_user = models.UserSignUp(
                first_name=booking.first_name,
                middle_name=booking.middle_name,
                last_name=booking.last_name,
                phone=booking.phone,
                role=models.UserRole.USER,
                password=None
            )
            user = await self._db_facade.signup(user=new_user)
        
        service = await self._db_facade.get_service_by_id(guid=booking.service_guid)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Услуга не найдена",
            )
        if service.datetime < datetime.datetime.now():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Услуга уже прошла",
            )
        cur_number_persons = await self._db_facade.get_cur_number_persons(service_id=booking.service_guid)
        if (booking.number_persons + cur_number_persons) > service.max_number_persons:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Нет свободных мест. В текущий момент уже забронировано мест: {str(cur_number_persons)}",
            )

        db_booking = await self._db_facade.create_booking(requester_id=requester_id, user_id=user.guid, booking=booking)
        await self._db_facade.commit()

        log.debug(f"Пользователь {requester_id}: бронь успешно создана")

        return db_booking

    async def get_booking_by_id(self, user_id: UUID4, booking_id: UUID4) -> models.BookingGet:
        """Получить услугу по id"""

        log.debug(f"Пользователь {user_id}: запрос на получение услуги по id: {booking_id}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.USER,
                                                                models.UserRole.WORKER,
                                                                models.UserRole.ADMIN))

        db_service = await self._db_facade.get_booking_by_id(guid=booking_id)

        log.debug(f"Пользователь {user_id}: бронь {booking_id} успешно получена")

        return db_service
    
    async def get_all_bookings(self, user_id: UUID4, limit: int, offset: int) -> List[models.BookingGet]:
        """Получить все брони"""

        log.debug(f"Пользователь {user_id}: запрос на получение всех броней")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER,
                                                                models.UserRole.ADMIN))

        db_bookings = await self._db_facade.get_all_bookings(limit=limit, offset=offset)

        log.debug(f"Пользователь {user_id}: все брони успешно получены")

        return db_bookings

    async def change_booking_status(self, user_id: UUID4, booking_id: UUID4, status: models.BookingStatusUpdate) -> models.BookingGet:
        """Изменить статус брони"""

        log.debug(f"Пользователь {user_id}: запрос на изменение статуса брони по id: {status.guid}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        await self._check_booking_exists_by_id(user_id=user_id, booking_id=status.guid)

        db_booking = await self._db_facade.change_booking_status(guid=booking_id, status=status.status)
        await self._db_facade.commit()

        log.debug(f"Пользователь {user_id}: статус брони {status.guid} успешно изменен")

        return db_booking

    async def change_booking(self, user_id: UUID4, booking_id: UUID4, booking: models.BookingUpdate) -> models.BookingGet:
        """Изменить бронь"""

        log.debug(f"Пользователь {user_id}: запрос на изменение брони по id: {booking_id}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        if not await self._check_booking_exists_by_id(user_id=user_id, booking_id=booking_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронь не найдена"
            )

        db_booking = await self._db_facade.change_booking(guid=booking_id, booking=booking)
        await self._db_facade.commit()

        log.debug(f"Пользователь {user_id}: бронь успешно изменена")

        return db_booking

    async def delete_booking(self, user_id: UUID4, booking_id: UUID4):
        """Удалить бронь"""

        log.debug(f"Пользователь {user_id}: запрос на удаление брони по id: {booking_id}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        if not await self._check_booking_exists_by_id(user_id=user_id, booking_id=booking_id):
            raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронь не найдена"
            )

        await self._db_facade.delete_booking(guid=booking_id)
        await self._db_facade.commit()

        log.debug(f"Пользователь {user_id}: бронь успешно удалена")

    # async def _check_booking_exists_by_user_and_service(self, user_id: UUID4, service_id: UUID4) -> bool:
    #     db_booking = await self._db_facade.get_booking_unique(
    #         user_id=user_id,
    #         service_id=service_id,
    #     )
    #     if db_booking:
    #         log.debug(f"Пользователь {user_id}: бронь уже существует")
    #         return True

    #     log.debug(f"Пользователь {user_id}: бронь не существует")
    #     return False

    async def _check_booking_exists_by_id(self, user_id: UUID4, booking_id: UUID4) -> bool:
        db_booking = await self._db_facade.get_booking_by_id(guid=booking_id)

        if db_booking:
            log.dubug(f"Пользователь {user_id}: бронь c id {booking_id} уже существует")
            return True

        log.debug(f"Пользователь {user_id}: бронь с id {booking_id} не существует")
        return False