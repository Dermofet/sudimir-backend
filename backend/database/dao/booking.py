from typing import Optional, List
from datetime import datetime as dt

from pydantic import UUID4
from sqlalchemy import BigInteger, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend import models
from backend.database import tables


class BookingDAO:
    """DAO для работы с бронью"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, booking: models.BookingCreate) -> models.BookingGet:
        """Создание брони"""

        db_booking = tables.Booking(**booking.dict())

        self._session.add(db_booking)
        await self._session.flush()
        await self._session.refresh(db_booking)

        return models.BookingGet.from_orm(db_booking)

    async def get_by_id(self, guid: UUID4) -> Optional[models.BookingGet]:
        """Получение брони по id"""

        query = select(tables.Booking).where(tables.Booking.guid == guid)
        db_booking = (await self._session.execute(query)).scalar()

        return models.BookingGet.from_orm(db_booking) if db_booking else None

    async def get_all_by_user_id(self, user_id: UUID4, limit: int, offset: int) -> List[models.BookingGet]:
        """Получение всех броней по id пользователя"""

        query = select(tables.Booking).where(tables.Booking.user_id == user_id).limit(limit).offset(offset)
        db_bookings = (await self._session.execute(query)).scalars().unique().all()

        return [models.BookingGet.from_orm(db_booking) for db_booking in db_bookings]

    async def change_status(self, guid: UUID4, status: models.BookingStatusType) -> models.BookingGet:
        """Изменение статуса брони"""

        query = select(tables.Booking).where(tables.Booking.guid == guid).update({"status": status})
        db_booking = (await self._session.execute(query)).scalar()

        return models.BookingGet.from_orm(db_booking) if db_booking else None

    async def change(self, guid: UUID4, booking: models.BookingUpdate) -> models.BookingGet:
        """Изменение брони"""

        query = select(tables.Booking).where(tables.Booking.guid == guid)
        db_booking = (await self._session.execute(query)).scalar()

        query = update(tables.Service).where(tables.Service.guid == guid).values(**booking.dict())
        await self._session.execute(query)

        await self._session.flush()
        await self._session.refresh(db_booking)

        return models.ServiceGet.from_orm(db_booking)

    async def delete(self, guid: UUID4) -> None:
        """Удаление брони"""

        query = delete(tables.Booking).where(tables.Booking.guid == guid)
        await self._session.execute(query)

        await self._session.flush()