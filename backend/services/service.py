from typing import List, Tuple, Union

from fastapi import Depends, HTTPException, status
from backend.logging import log
from pydantic import UUID4

from backend import models
from backend.database.facade import DBFacadeInterface, get_db_facade
from backend.utils.user import check_user_existence_and_access


class ServiceService:
    def __init__(self, db_facade: DBFacadeInterface = Depends(get_db_facade)):
        self._db_facade = db_facade

    async def create_service(self, user_id: UUID4, service: models.ServiceCreate) -> models.ServiceGet:
        """Создать услугу"""

        log.debug(f"Пользователь {user_id}: запрос на создание услуги")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        await self._check_service_exists_by_all_fields(user_id=user_id, service=service)

        db_service = await self._db_facade.create_service(service=service)
        await self._db_facade.commit()

        log.debug(f"Пользователь {user_id}: услуга успешно создана")

        return db_service

    async def get_service_by_id(self, service_id: UUID4) -> models.ServiceGet:
        """Получить услугу по id"""

        log.debug(f"Запрос на получение услуги по id: {service_id}")

        db_service = await self._db_facade.get_service_by_id(guid=service_id)

        log.debug(f"Услуга {service_id} успешно получена")

        return db_service

    async def get_all(self, limit: int, offset: int) -> List[models.ServiceGet]:
        """Получение списка услуг"""

        log.debug("Запрос на получение списка услуг")

        db_services = await self._db_facade.get_services(limit=limit, offset=offset)

        log.debug("Услуги слуги успешно получены")

        return db_services

    async def change_service(self, user_id: UUID4, service_id: UUID4, service: models.ServiceUpdate) -> models.ServiceGet:
        """Изменить услугу"""

        log.debug(f"Пользователь {user_id}: запрос на изменение услуги по id: {service_id}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        await self._check_service_exists_by_id(user_id=user_id, service_id=service_id)

        db_service = await self._db_facade.change_service(guid=service_id, service=service)
        await self._db_facade.commit()

        log.debug(f"Пользователь {user_id}: услуга успешно изменена")

        return db_service

    async def delete_service(self, user_id: UUID4, service_id: UUID4):
        """Удалить услугу"""

        log.debug(f"Пользователь {user_id}: запрос на удаление услуги по id: {service_id}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        await self._check_service_exists_by_id(user_id=user_id, service_id=service_id)

        await self._db_facade.delete_service(guid=service_id)
        await self._db_facade.commit()

        log.debug(f"Пользователь {user_id}: услуга успешно удалена")

    async def _check_service_exists_by_all_fields(self, user_id: UUID4, service: models.ServiceCreate) -> None:
        db_service = await self._db_facade.get_service_by_all_fields(name=service.name,
                                                                     price=service.price,
                                                                     datetime=service.datetime,
                                                                     max_number_persons=service.max_number_persons,
                                                                     type=service.type)
        if db_service:
            log.warning(f"Пользователь {user_id}: услуга уже существует")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такая услуга уже существует",
            )

    async def _check_service_exists_by_id(self, user_id: UUID4, service_id: UUID4) -> None:
        db_service = await self._db_facade.get_service_by_id(guid=service_id)

        if not db_service:
            log.warning(f"Пользователь {user_id}: услуга c id {service_id} не найдена")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Услуга не найдена",
            )