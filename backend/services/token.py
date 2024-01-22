from datetime import datetime, timedelta, timezone
from typing import Dict, Union
from uuid import uuid4

from jose import jwt

from backend import models
from backend.config import config


class TokenService:
    async def generate_auth_token(self, user: models.UserGet) -> models.Token:
        """Генерация JWT токена"""

        payload = self._get_token_payload(user=user)
        token = jwt.encode(
            claims=payload,
            key=config.JWT_SECRET,
            algorithm=config.JWT_ALGORITHM,
        )
        return models.Token(access_token=token)

    @staticmethod
    def _get_token_payload(user: models.UserGet) -> Dict[str, Union[datetime, str]]:
        """Генерация данных для JWT токена"""

        created_at = datetime.now(timezone.utc)
        # expires_at = created_at + timedelta(seconds=config.JWT_EXPIRES_AT)
        expires_at = created_at + timedelta(days=365*100) # non expired token 
        return {
            "exp": expires_at,
            "iat": created_at,
            "jti": str(uuid4()),
            "sub": str(user.guid),
        }
