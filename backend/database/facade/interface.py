from abc import ABC, abstractmethod
from typing import List
from datetime import datetime as dt

from pydantic import UUID4

from backend import models


class DBFacadeInterface(ABC):
    """Интерфейс фасада базы данных"""

    @abstractmethod
    async def commit(self) -> None:
        """Применение изменений"""
        ...

    @abstractmethod
    async def is_db_alive(self) -> bool:
        """Проверка работы БД"""
        ...

    @abstractmethod
    async def signup(self, user: models.UserSignUp) -> models.UserGet:
        """Регистрация нового пользователя"""
        ...

    @abstractmethod
    async def get_user_by_id(self, guid: UUID4) -> models.UserGet:
        """Получения пользователя по id"""
        ...

    @abstractmethod
    async def get_all_users(self, limit: int, offset: int) -> List[models.UserGet]:
        """Получение списка пользователей"""
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> models.UserGet:
        """Получения пользователя по email"""
        ...

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> models.UserGet:
        """Получения пользователя по номеру телефона"""
        ...

    @abstractmethod
    async def get_all_users_with_role(self, limit: int, offset: int, role: models.UserRole) -> List[models.UserGet]:
        """Получение списка пользователей"""
        ...

    @abstractmethod
    async def change_user(self, guid: UUID4, user: models.UserUpdate) -> models.UserGet:
        """Изменения пользователя"""
        ...

    @abstractmethod
    async def delete_user(self, guid: UUID4):
        """Удаления пользователя"""
        ...

    @abstractmethod
    async def create_service(self, service: models.ServiceCreate) -> models.ServiceGet:
        """Создания услуги"""
        ...

    @abstractmethod
    async def get_service_by_id(self, guid: UUID4) -> models.ServiceGet:
        """Получение услуги по id"""
        ...

    @abstractmethod
    async def get_service_by_all_fields(self, name: str, price: int, datetime: dt, max_number_persons: int, type: str) -> models.ServiceGet:
        """Получение услуги по всем полям"""
        ...

    @abstractmethod
    async def get_all_services(self, limit: int, offset: int) -> List[models.ServiceGetAll]:
        """Получение списка услуг"""
        ...

    @abstractmethod
    async def change_service(self, guid: UUID4, service: models.ServiceUpdate):
        """Изменение услуги"""
        ...

    @abstractmethod
    async def delete_service(self, guid: UUID4):
        """Удаление услуги"""
        ...

    @abstractmethod
    async def create_booking(self, requester_id: UUID4, user_id: UUID4, booking: models.BookingCreate) -> models.BookingGet:
        """Создание бронирования"""
        ...

    @abstractmethod
    async def get_booking_by_id(self, guid: UUID4) -> models.BookingGet:
        """Получение бронирования по id"""
        ...

    @abstractmethod
    async def get_all_bookings_by_user_id(self, user_id: UUID4, limit: int, offset: int) -> List[models.BookingGet]:
        """Получение списка бронирований по id пользователя"""
        ...

    @abstractmethod
    async def change_booking_status(self, guid: UUID4, status: models.BookingStatusUpdate) -> models.BookingGet:
        """Изменение статуса бронирования"""
        ...

    @abstractmethod
    async def change_booking(self, guid: UUID4, booking: models.BookingUpdate) -> models.BookingGet:
        """Изменение бронирования"""
        ...

    @abstractmethod
    async def delete_booking(self, guid: UUID4):
        """Удаление бронирования"""
        ...
