from fastapi import HTTPException, status
from typing import  Tuple
from pydantic import UUID4

from backend import models
from backend.logging import log


async def check_user_existence_and_access(user: models.UserGet, roles: Tuple[models.UserRole, ...]) -> None:
    if not user:
        log.warning(f"Попытка получения пользователя с несуществующим id: {user.guid}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь не существует",
        )

    if user.role not in roles:
        log.warning(f"Пользователь {user.guid}: недостаточно прав для выполнения этого действия")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не имеет прав на выполнение этого действия",
        )