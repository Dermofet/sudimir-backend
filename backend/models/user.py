from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import field_validator, UUID4, EmailStr, Field
import phonenumbers

from backend.models.utils import ApiModel


class UserRole(str, Enum):
    ADMIN = "admin"
    WORKER = "worker"
    USER = "user"


class UserBase(ApiModel):
    first_name:  Optional[str] = Field(..., description="Имя")
    last_name:  Optional[str] = Field(..., description="Фамилия")
    middle_name: Optional[str] = Field(None, description="Отчество")
    email: Optional[EmailStr] = Field(None, description="Почта")
    phone: str = Field(..., description="Номер телефона")
    role: UserRole = Field(..., description="Роль пользователя")

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, value):
        try:
            phone_number = phonenumbers.parse(value)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise ValueError('Некорректный номер телефона') from e

        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError('Некорректный номер телефона')

        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

class UserSignIn(ApiModel):
    phone: Optional[str] = Field(None, description="Номер телефона")
    email: Optional[EmailStr] = Field(None, description="Почта")
    password: str = Field(..., description="Пароль")

    @field_validator('phone')
    def validate_phone_number(cls, value):
        if not value:
            return value

        try:
            phone_number = phonenumbers.parse(value)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise ValueError('Некорректный номер телефона') from e

        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError('Некорректный номер телефона')

        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    @field_validator('email')
    def validate_email(cls, v, values):
        if not v and not values.get('phone'):
            raise ValueError("Одно из полей 'phone' или 'email' должно быть заполнено")
        return v

class UserSignUp(UserBase):
    password: Optional[str] = Field(..., description="Пароль")

class UserChangePassword(ApiModel):
    guid: UUID4 = Field(..., description="Идентификатор пользователя")
    password: str = Field(..., description="Пароль")

class UserForgotPassword(ApiModel):
    email: Optional[EmailStr] = Field(None, description="Почта")
    phone: Optional[str] = Field(None, description="Номер телефона")

    @field_validator('phone')
    def validate_phone_number(cls, value):
        if not value:
            return value

        try:
            phone_number = phonenumbers.parse(value)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise ValueError('Некорректный номер телефона') from e

        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError('Некорректный номер телефона')

        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    @field_validator('email')
    def validate_email(cls, v, values):
        if not v and not values.get('phone'):
            raise ValueError("Одно из полей 'phone' или 'email' должно быть заполнено")
        return v
    
class UserUpdate(UserBase):
    pass

class UserPatch(UserUpdate):
    pass

class UserGet(UserSignUp):
    guid: UUID4 = Field(..., description="Идентификатор пользователя")
    created_at: datetime = Field(..., description="Время создания пользователя в формате RFC-3339")
    updated_at: datetime = Field(..., description="Время последнего обновления пользователя в формате RFC-3339")

class UserGetWithoutPassword(UserBase):
    pass
