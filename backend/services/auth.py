from typing import Union

from fastapi import Depends, HTTPException, status
from backend.logging import log
from pydantic import UUID4
from passlib.hash import bcrypt

from backend import models
from backend.database.facade import DBFacadeInterface, get_db_facade
from backend.services.token import TokenService


class AuthService:
    def __init__(self, db_facade: DBFacadeInterface = Depends(get_db_facade)):
        self._db_facade = db_facade
        self._token_service = TokenService()

    async def signup(self, user: models.UserSignUp) -> models.Token:
        """Регистрация нового пользователя"""

        log.debug(f"Регистрация нового пользователя: {user.phone or user.email}")

        if not (exc := await self._check_user_exists(user=user)):
            raise exc

        hashed_password = self._crypt_password(password=user.password)
        user.password = hashed_password

        new_user = await self._db_facade.signup(user=user)
        await self._db_facade.commit()

        token = await self._token_service.generate_auth_token(user=new_user)

        log.debug(f"Пользователь {user.phone} успешно зарегистрирован")

        return token

    async def signin(self, user: models.UserSignIn) -> models.Token:
        """Авторизация пользователя"""

        log.debug(f"Авторизация Пользователя {user.email or user.phone}")

        if await self._check_user_exists(user=user):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")

        db_user = await self._db_facade.get_user_by_phone(user.phone) or \
                  await self._db_facade.get_user_by_email(user.email)

        await self._check_user_password(user=user, db_user=db_user)

        token = await self._token_service.generate_auth_token(user=db_user)
        log.debug(f"Пользователь {user.email or user.phone} успешно авторизован")

        return token

    async def forgot_password(self, user: models.UserForgotPassword) -> models.UserGet:
        """Получить пользователя без пароля"""

        log.debug(f"Получение пользователя без пароля: {user.email or user.phone}")

        if await self._check_user_exists(user=user):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        log.debug(f"Пользователь без пароля {user.email or user.phone} успешно получен")

        return await self._db_facade.get_user_by_phone(user.phone) \
            or await self._db_facade.get_user_by_email(user.email)

    async def change_password(self, user: models.UserChangePassword) -> models.UserGet:
        """Изменить пароль пользователя"""

        log.debug(f"Пользователь {user.guid}: изменение пароля")

        db_user = await self._db_facade.get_user_by_id(guid=user.guid)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        db_user.password = self._crypt_password(password=user.password)

        await self._db_facade.commit()

        token = await self._token_service.generate_auth_token(user=db_user)

        log.debug(f"Пользователь {user.guid}: пароль успешно изменен")

        return token

    @staticmethod
    def _crypt_password(password: str) -> str:
        """Шифрование пароля"""

        return bcrypt.hash(password)

    @staticmethod
    async def _check_user_password(user: models.UserSignIn, db_user: models.UserGet) -> None:
        """Проверка правильности пароля пользователя"""

        if not bcrypt.verify(user.password, db_user.password):
            log.warning(f"Попытка входа пользователя {user.email or user.phone} c неверным паролем")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")

    async def _check_user_exists(self, user: Union[models.UserSignIn, models.UserSignUp, models.UserForgotPassword]) -> HTTPException:
        """Проверка пользователя на существование"""

        if user.phone and not await self._db_facade.get_user_by_phone(user.phone):
            log.warning(f"Пользователь с номером телефона {user.phone} не существует")
            return HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Пользователь с таким номером телефона не существует")

        elif not await self._db_facade.get_user_by_email(user.email):
            log.warning(f"Пользователь с email {user.email} не существует")
            return HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Пользователь с такой почтой уже существует")

        return None