from datetime import datetime as dt
from enum import Enum
from typing import Optional
import phonenumbers
from pydantic import ConfigDict, UUID4, Field, field_validator
from backend.models.utils import ApiModel


class BookingStatusType(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'


class BookingStatusUpdate(ApiModel):
    guid: UUID4 = Field(..., description="Идентификатор брони")
    status: BookingStatusType = Field(..., description="Статус брони")


class BookingBase(ApiModel):
    service_guid: UUID4 = Field(..., description="Идентификатор услуги")
    number_persons: int = Field(..., description="Количество человек")
    status: BookingStatusType = Field(..., description="Статус брони")

    model_config = ConfigDict(json_encoders={
        dt: lambda d: d.strftime('%d-%m-%Y %H:%M')
    })


class BookingCreate(BookingBase):
    first_name: Optional[str] = Field(..., description="Имя пользователя")
    middle_name: Optional[str] = Field(None, description="Отчество пользователя")
    last_name: Optional[str] = Field(..., description="Фамилия пользователя")

    phone: str = Field(..., description="Номер телефона пользователя")

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


class BookingUpdate(BookingBase):
    pass


class BookingPatch(BookingBase):
    pass


class BookingGet(BookingBase):
    guid: UUID4 = Field(..., description="Идентификатор услуги")
    service_guid: UUID4 = Field(..., description="Идентификатор услуги")
    user_guid: UUID4 = Field(..., description="Идентификатор пользователя")

    user_created: UUID4 = Field(..., description="Идентификатор пользователя, создавшего услугу")
    user_updated: UUID4 = Field(..., description="Идентификатор пользователя, обновившего услугу")

    created_at: dt = Field(..., description="Время создания услуги в формате RFC-3339")
    updated_at: dt = Field(..., description="Время последнего обновления услуги в формате RFC-3339")
