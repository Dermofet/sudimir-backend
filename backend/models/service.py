from datetime import datetime as dt
from enum import Enum
from typing import Optional
from pydantic import field_validator, ConfigDict, UUID4, Field
from backend.models.utils import ApiModel


class ServiceType(str, Enum):
    TOUR = "tour"
    RENT = "rent"


class ServiceBase(ApiModel):
    name: str = Field(..., description="Название")
    description: str = Field(..., description="Описание")
    price: int = Field(..., description="Цена")
    duration: str = Field(..., description="Продолжительность услуги")
    datetime: dt = Field(..., description="Дата и время проведения услуги")
    max_number_persons: int = Field(..., description="Максимальное количество человек, на которое рассчитана услуга")
    type: str = Field(..., description="Тип услуги")

    @field_validator('type', mode="before")
    def validate_service_type(cls, v):
        if ServiceType(v) not in ServiceType:
            raise ValueError('Некорректный тип услуги')
        return v

    @field_validator('datetime', mode="before")
    def validate_service_datetime(cls, v):
        if isinstance(v, str):
            return dt.strptime(v, '%d-%m-%Y %H:%M')
        elif isinstance(v, dt):
            return dt.strptime(v.strftime('%d-%m-%Y %H:%M'), '%d-%m-%Y %H:%M')
        else:
            raise ValueError('Некорректный формат')

    model_config = ConfigDict(json_encoders={
        dt: lambda d: d.strftime('%d-%m-%Y %H:%M')
    })



class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServicePatch(ServiceBase):
    pass


class ServiceGet(ServiceBase):
    guid: UUID4 = Field(..., description="Идентификатор услуги")
    created_at: dt = Field(..., description="Время создания услуги в формате RFC-3339")
    updated_at: dt = Field(..., description="Время последнего услуги сер в формате RFC-3339")
