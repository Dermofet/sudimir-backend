from fastapi import status, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from backend.config import config

schema_bearer = HTTPBearer()


async def verify_access_token(access_token: HTTPAuthorizationCredentials = Depends(schema_bearer)):
    try:
        jwt.decode(
            access_token.credentials,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Неверный токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e