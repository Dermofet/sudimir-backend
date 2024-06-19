import json
from confluent_kafka import Consumer, KafkaException
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.services.booking import BookingService

from typing import Dict, List

from fastapi import Depends
from pydantic import UUID4

from backend import config, models
from backend.services.booking import BookingService
from backend.utils.auth import get_user_from_access_token
from jose import jwt

schema_bearer = HTTPBearer()

consumer = Consumer('booking', bootstrap_servers='localhost:9092')

'''
{
    'command': 'create',
    'token': [your_token]
    'value': {
        ...
    }
}
'''
def read_kafka():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # ожидание сообщения
            if msg is None:                   # если сообщений нет
                continue
            if msg.error():                   # обработка ошибок
                raise KafkaException(msg.error())
            
            value = json.loads(msg.value())
            
            if value['command'] == 'create_booking':
                create_booking(
                    booking=models.BookingCreate.model_validate_json(value['value']),
                    requester_id=verify_access_token(value['token']),
                )
            elif value['command'] == 'get_booking':
                get_booking(
                    id_=value['value']['id'],
                    user_id=verify_access_token(value['token']),
                )
            elif value['command'] == 'get_all_bookings':
                get_all_bookings(
                    limit=value['value']['limit'],
                    offset=value['value']['offset'],
                    user_id=verify_access_token(value['token']),
                )
            elif value['command'] == 'change_booking_status':
                change_booking_status(
                    id_=value['value']['id'],
                    status=models.BookingStatusUpdate(
                        guid=value['value']['id'],
                        status=value['value']['status'],
                    ),
                    user_id=verify_access_token(value['token']),
                )
            elif value['command'] == 'change_booking':
                change_booking(
                    id_=value['value']['id'],
                    booking=models.BookingUpdate.model_validate_json(value['value']['booking']),
                    user_id=verify_access_token(value['token']),
                )
            elif value['command'] == 'delete_booking':
                delete_booking(
                    id_=value['value']['id'],
                    user_id=verify_access_token(value['token']),
                )
                
    except KeyboardInterrupt:
        pass 
    finally:
        consumer.close()
    
async def verify_access_token(access_token: HTTPAuthorizationCredentials = Depends(schema_bearer)):
    try:
        info = jwt.decode(
            access_token.credentials,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        return info["sub"]
    except Exception:
        raise Exception("Неверный токен авторизации")

async def create_booking(
    booking: models.BookingCreate,
    requester_id: UUID4,
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.create_booking(requester_id=requester_id, booking=booking)


async def get_booking(
    id_: UUID4,
    user_id: UUID4,
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.get_booking_by_id(user_id=user_id, booking_id=id_)


async def get_all_bookings(
    limit: int,
    offset: int,
    user_id: UUID4,
    booking_service: BookingService = Depends(),
) -> Dict[str, List[models.BookingGet]]:
    result = await booking_service.get_all_bookings(user_id=user_id, limit=limit, offset=offset)
    return {"bookings": result}


async def change_booking_status(
    id_: UUID4,
    status: models.BookingStatusUpdate,
    user_id: UUID4,
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.change_booking_status(user_id=user_id, booking_id=id_, status=status)


async def change_booking(
    id_: UUID4,
    booking: models.BookingUpdate,
    user_id: UUID4,
    booking_service: BookingService = Depends(),
) -> models.BookingGet:
    return await booking_service.change_booking(user_id=user_id, booking_id=id_, booking=booking)


async def delete_booking(
    booking_id: UUID4,
    user_id: UUID4,
    booking_service: BookingService = Depends(),
):
    return await booking_service.delete_booking(user_id=user_id, booking_id=booking_id)