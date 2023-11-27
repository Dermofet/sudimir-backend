from fastapi import Depends

from backend.database.facade.facade import DBFacade
from backend.database.facade.interface import DBFacadeInterface


def get_db_facade(db_facade: DBFacade = Depends(DBFacade)) -> DBFacadeInterface:
    return db_facade