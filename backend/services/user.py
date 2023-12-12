from typing import List

from fastapi import Depends, HTTPException
from backend.logging import log
from pydantic import UUID4

from backend import models
from backend.database.facade import DBFacadeInterface, get_db_facade
from backend.utils.user import check_user_existence_and_access


class UserService:
    def __init__(self, db_facade: DBFacadeInterface = Depends(get_db_facade)):
        self._db_facade = db_facade

    async def create_user(self, requester_id: UUID4, user: models.UserSignUp) -> models.UserGet:
        """Создать пользователя"""

        log.debug(f"Пользователь {requester_id}: запрос на создание пользователя: {user}")

        requester = await self._db_facade.get_user_by_id(guid=requester_id)
        await check_user_existence_and_access(user_id=requester_id, user=requester, roles=(models.UserRole.ADMIN))

        db_user = await self._db_facade.signup(user=user)
        await self._db_facade.commit()

        log.debug(f"Пользователь {requester_id}: создание пользователя: {user}")

        return db_user

    async def get_all_users(self, user_id: UUID4, limit: int, offset: int) -> List[models.UserGet]:
        """Получить список пользователей"""

        log.debug(f"Пользователь {user_id}: запрос на получение всех пользователей: {limit}, {offset}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user_id=user_id, user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        db_users = await self._db_facade.get_all_users(limit=limit, offset=offset)

        log.debug(f"Пользователь {user_id}: успешно получены пользователи")

        return db_users

    async def get_user_by_id(self, user_id: UUID4, guid: UUID4) -> models.UserGet:
        """Получить пользователя по id"""

        log.debug(f"Пользователь {user_id}: запрос на получение пользователя по id: {guid}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user_id=user_id, user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        db_user = await self._db_facade.get_user_by_id(guid=guid)

        log.debug(f"Пользователь {guid} успешно получен")

        print(db_user)
        return db_user

    async def get_user_by_email(self, user_id: UUID4, email: str) -> models.UserGet:
        """Получить пользователя по email"""

        log.debug(f"Пользователь {user_id}: запрос на получение пользователя по email: {email}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user_id=user_id, user=user, roles=(models.UserRole.WORKER, models.UserRole.ADMIN))

        db_user = await self._db_facade.get_user_by_email(email=email)

        log.debug(f"Пользователь {email} успешно получен")

        return db_user

    async def get_all_users_with_role(self, user_id: UUID4, limit: int, offset: int, role: models.UserRole) -> List[models.UserGet]:
        """Получить список пользователей с определенным ролем"""

        log.debug(f"Пользователь {user_id}: запрос на получение всех пользователей с определенным ролем: {limit}, {offset}, {role}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user_id=user_id, user=user, roles=models.UserRole.ADMIN)

        db_users = await self._db_facade.get_all_users_with_role(limit=limit, offset=offset, role=role)

        log.debug(f"Пользователь {user_id}: успешно получены пользователи с ролью {role}")

        return db_users

    async def get_all_bookings_by_id(self, recipient_id: UUID4, user_id: UUID4, limit: int, offset: int) -> List[models.BookingGet]:
        """Получить список брони по id пользователя"""

        log.debug(f"Пользователь {recipient_id}: запрос на получение всех бронирований пользователя {user_id}: {limit}, {offset}")

        user = await self._db_facade.get_user_by_id(guid=recipient_id)
        await check_user_existence_and_access(user_id=user_id, user=user, roles=(models.UserRole.ADMIN,
                                                                models.UserRole.WORKER,
                                                                models.UserRole.USER))

        db_bookings = await self._db_facade.get_all_bookings_by_user_id(user_id=user_id, limit=limit, offset=offset)

        log.debug(f"Пользователь {recipient_id}: успешно получены бронирования")

        return db_bookings

    async def change_user(self, user_id: UUID4, guid: UUID4, user: models.UserUpdate) -> models.UserGet:
        """Изменить пользователя"""

        log.debug(f"Пользователь {user_id}: запрос на изменение пользователя по id: {guid}")

        user = await self._db_facade.get_user_by_id(guid=user_id)
        await check_user_existence_and_access(user_id=user_id, user=user, roles=models.UserRole.ADMIN)

        db_user = await self._db_facade.change_user(guid=user_id, user=user)
        await self._db_facade.commit()

        log.debug(f"Пользователь {guid} успешно изменен")

        return db_user

    async def delete_user(self, user_id: UUID4, guid: UUID4):
        """Удалить пользователя"""

        log.debug(f"Пользователь {user_id}: запрос на удаление пользователя по id: {guid}")

        if user_id != guid:
            user = await self._db_facade.get_user_by_id(guid=user_id)
            await check_user_existence_and_access(user_id=user_id, user=user, roles=models.UserRole.ADMIN)

            await self._db_facade.delete_user(guid=guid)
            await self._db_facade.commit()
        else:
            raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")

        log.debug(f"Пользователь {guid} успешно удален")
