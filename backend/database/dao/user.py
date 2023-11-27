from typing import Optional, List

from pydantic import UUID4
from sqlalchemy import BigInteger, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend import models
from backend.database import tables


class UserDAO:
    """DAO для работы с пользователями"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: models.UserSignUp) -> models.UserGet:
        """Создание пользователя"""

        db_user = tables.User(**user.dict())

        self._session.add(db_user)
        await self._session.flush()
        await self._session.refresh(db_user)

        return models.UserGet.from_orm(db_user)

    async def get_by_email(self, email: str) -> Optional[models.UserGet]:
        """Получение пользователя по email"""

        query = select(tables.User).where(tables.User.email == email)
        db_user = (await self._session.execute(query)).scalar()

        return models.UserGet.from_orm(db_user) if db_user else None

    async def get_by_phone(self, phone: str) -> Optional[models.UserGet]:
        """Получение пользователя по номеру телефона"""

        query = select(tables.User).where(tables.User.phone == phone)
        db_user = (await self._session.execute(query)).scalar()

        return models.UserGet.from_orm(db_user) if db_user else None

    async def get_by_id(self, guid: UUID4) -> Optional[models.UserGet]:
        """Получение пользователя по id"""

        query = select(tables.User).where(tables.User.guid == guid)
        db_user = (await self._session.execute(query)).scalar()

        return models.UserGet.from_orm(db_user) if db_user else None

    async def get_all(self, limit: int, offset:int) -> Optional[models.UserGet]:
        """Получение списка пользователей"""

        query = select(tables.User).limit(limit).offset(offset)
        db_users = (await self._session.execute(query)).scalars().unique().all()

        return [models.UserGet.from_orm(db_user) for db_user in db_users]

    async def get_all_with_role(self, limit: int, offset:int, role: models.UserRole) -> List[models.UserGet]:
        """Получение всех пользователей с определенной ролью"""

        query = select(tables.User).where(tables.User.role == role).limit(limit).offset(offset)
        db_users = (await self._session.execute(query)).scalars().unique().all()

        return [models.UserGet.from_orm(db_user) for db_user in db_users]

    async def change(self, guid: UUID4, user: models.UserUpdate) -> models.UserGet:
        """Изменение пользователя"""

        db_user = (await self._session.execute(select(tables.User).where(tables.User.guid == guid))).scalar()

        query = update(tables.User).where(tables.User.guid == guid).values(**user.dict())
        await self._session.execute(query)

        await self._session.flush()
        await self._session.refresh(db_user)

        return models.UserGet.from_orm(db_user)

    async def delete(self, guid: UUID4) -> None:
        """Удаление пользователя"""

        query = delete(tables.User).where(tables.User.guid == guid)
        await self._session.execute(query)

        await self._session.flush()
