from datetime import datetime as dt
from enum import Enum
from pydantic import ConfigDict, UUID4, Field
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
    pass


class BookingUpdate(BookingBase):
    pass


class BookingPatch(BookingBase):
    pass


class BookingGet(BookingBase):
    guid: UUID4 = Field(..., description="Идентификатор услуги")
    service_guid: UUID4 = Field(..., description="Идентификатор услуги")
    user_guid: UUID4 = Field(..., description="Идентификатор пользователя")

    status: str = Field(..., description="Статус")
    number_persons: int = Field(..., description="Количество человек, которое будет на услуге")

    user_created: UUID4 = Field(..., description="Идентификатор пользователя, создавшего услугу")
    user_updated: UUID4 = Field(..., description="Идентификатор пользователя, обновившего услугу")

    created_at: dt = Field(..., description="Время создания услуги в формате RFC-3339")
    updated_at: dt = Field(..., description="Время последнего обновления услуги в формате RFC-3339")
