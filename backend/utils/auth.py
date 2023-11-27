from fastapi import Request
from pydantic import UUID4
from jose import jwt

from backend.config import config


def get_user_from_access_token(request: Request) -> UUID4:
    access_token = request.headers["Authorization"].split()[1]
    info = jwt.decode(
        access_token,
        config.JWT_SECRET,
        algorithms=[config.JWT_ALGORITHM],
        options={"verify_aud": False},
    )
    return info["sub"]
