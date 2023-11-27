from pydantic import Field

from backend.models.utils import ApiModel


class Token(ApiModel):
    access_token: str = Field(..., description="JWT токен")
