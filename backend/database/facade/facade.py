from datetime import datetime as dt
from decimal import Decimal
from typing import List

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from backend import models
from backend.database.connection import get_session
from backend.database.dao import *
from backend.database.dao.booking import BookingDAO
from backend.database.facade.interface import DBFacadeInterface


class DBFacade(DBFacadeInterface):
    """Фасад для работы с базой данных"""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session
        self._user_dao = UserDAO(session=session)
        self._service_dao = ServiceDAO(session=session)
        self._booking_dao = BookingDAO(session=session)

    async def commit(self) -> None:
        """Применение изменений"""

        await self._session.commit()

    async def is_db_alive(self) -> bool:
        """Проверка работы БД"""

        try:
            await self._session.execute("SELECT version_num FROM alembic_version")
        except Exception:
            return False
        return True

    async def signup(self, user: models.UserSignUp) -> models.UserGet:
        """Создание пользователя"""

        return await self._user_dao.create(user=user)

    async def get_all_users(self, limit: int, offset: int) -> List[models.UserGet]:
        """Получение списка пользователей"""

        return await self._user_dao.get_all(limit=limit, offset=offset)

    async def get_user_by_id(self, guid: UUID4) -> models.UserGet:
        """Получения пользователя по id"""

        return await self._user_dao.get_by_id(guid=guid)

    async def get_user_by_email(self, email: str) -> models.UserGet:
        """Получения пользователя по email"""

        return await self._user_dao.get_by_email(email=email)

    async def get_user_by_phone(self, phone: str) -> models.UserGet:
        """Получения пользователя по номеру телефона"""

        return await self._user_dao.get_by_phone(phone=phone)

    async def get_all_users_with_role(self, limit: int, offset: int, role: models.UserRole) -> List[models.UserGet]:
        """Получение всех пользователей с определенной ролью"""

        return await self._user_dao.get_all_with_role(limit=limit, offset=offset, role=role)

    async def change_user(self, guid: UUID4, user: models.UserUpdate) -> models.UserGet:
        """Изменения пользователя"""

        return await self._user_dao.change(guid=guid, user=user)

    async def delete_user(self, guid: UUID4):
        """Удаления пользователя"""

        return await self._user_dao.delete(guid=guid)

    async def create_service(self, service: models.ServiceCreate) -> models.ServiceGet:
        """Создания услуги"""

        return await self._service_dao.create(service=service)

    async def get_service_by_id(self, guid: UUID4) -> models.ServiceGet:
        """Получение услуги по id"""

        return await self._service_dao.get_by_id(guid=guid)

    async def get_service_by_all_fields(self, name: str, price: int, datetime: dt, max_number_persons: int,
                                        type: str) -> models.ServiceGet:
        """Получение услуги по всем полям"""

        return await self._service_dao.get_by_all_fields(name=name, price=price, datetime=datetime,
                                                         max_number_persons=max_number_persons, type=type)

    async def get_all_services(self, limit: int, offset: int) -> List[models.ServiceGet]:
        """Получение списка услуг"""

        return await self._service_dao.get_all(limit=limit, offset=offset)

    async def change_service(self, guid: UUID4, _service: models.ServiceUpdate):
        """Изменение услуги"""

        return await self._service_dao.change(guid=guid, service=_service)

    async def delete_service(self, guid: UUID4):
        """Удаление услуги"""

        return await self._service_dao.delete(guid=guid)

    async def create_booking(self, requester_id: UUID4, user_id: UUID4, booking: models.BookingCreate) -> models.BookingGet:
        """Создание брони"""

        return await self._booking_dao.create(requester_id=requester_id, user_id=user_id, booking=booking)

    async def get_booking_by_id(self, guid: UUID4) -> models.BookingGet:
        """Получение брони по id"""

        return await self._booking_dao.get_by_id(guid=guid)

    async def get_all_bookings_by_user_id(self, user_id: UUID4, limit: int, offset: int) -> List[models.BookingGet]:
        """Получение всех бронирований по id пользователя"""

        return await self._booking_dao.get_all_by_user_id(user_id=user_id, limit=limit, offset=offset)

    async def change_booking_status(self, guid: UUID4, status: models.BookingStatusType) -> models.BookingGet:
        """Изменение статуса брони"""

        return await self._booking_dao.change_status(guid=guid, status=status)

    async def change_booking(self, guid: UUID4, booking: models.BookingUpdate) -> models.BookingGet:
        """Изменение брони"""

        return await self._booking_dao.change(guid=guid, booking=booking)

    async def delete_booking(self, guid: UUID4):
        """Удаление брони"""

        return await self._booking_dao.delete(guid=guid)
