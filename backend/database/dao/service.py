# from typing import Optional, List
# from datetime import datetime as dt

# from pydantic import UUID4
# from sqlalchemy import BigInteger, select, update, delete
# from sqlalchemy.ext.asyncio import AsyncSession

# from backend import models
# from backend.database import tables


# class ServiceDAO:
#     """DAO для работы с услугами"""

#     def __init__(self, session: AsyncSession):
#         self._session = session

#     async def create(self, service: models.ServiceCreate) -> models.ServiceGet:
#         """Создание услуги"""

#         db_service = tables.Service(**service.model_dump())

#         self._session.add(db_service)
#         await self._session.flush()
#         await self._session.refresh(db_service)

#         return models.ServiceGet.model_validate(db_service) if db_service else None

#     async def get_by_id(self, guid: UUID4) -> Optional[models.ServiceGet]:
#         """Получение услуги по id"""

#         query = select(tables.Service).where(tables.Service.guid == guid)
#         db_service = (await self._session.execute(query)).scalar()

#         return models.ServiceGet.model_validate(db_service) if db_service else None

#     async def get_by_all_fields(self, name: str, price: int, datetime: dt, max_number_persons: int, type: str) -> Optional[models.ServiceGet]:
#         """Получение услуги по полям"""

#         query = select(tables.Service).where(
#             tables.Service.name == name,
#             tables.Service.price == price,
#             tables.Service.datetime == datetime,
#             tables.Service.max_number_persons == max_number_persons,
#             tables.Service.type == type
#         )
#         db_service = (await self._session.execute(query)).scalar()

#         return models.ServiceGet.model_validate(db_service) if db_service else None

#     async def get_all(self, limit: int, offset: int) -> List[models.ServiceGet]:
#         """Получение списка услуг"""

#         query = select(tables.Service).limit(limit).offset(offset)
#         db_services = await self._session.execute(query)

#         return [models.ServiceGet.model_validate(db_service) for db_service in db_services.scalars().unique().all()]

#     async def change(self, guid: UUID4, service: models.ServiceUpdate) -> models.ServiceGet:
#         """Изменение услуги"""

#         db_service = (await self._session.execute(select(tables.Service).where(tables.Service.guid == guid))).scalar()

#         query = update(tables.Service).where(tables.Service.guid == guid).values(**service.model_dump())
#         await self._session.execute(query)

#         await self._session.flush()
#         await self._session.refresh(db_service)

#         return models.ServiceGet.model_validate(db_service)

#     async def delete(self, guid: UUID4) -> None:
#         """Удаление услуги"""

#         query = delete(tables.Booking).where(tables.Booking.service_guid == guid)
#         await self._session.execute(query)
        
#         query = delete(tables.Service).where(tables.Service.guid == guid)
#         await self._session.execute(query)

#         await self._session.flush()
