# from abc import ABC, abstractmethod 
# import aioredis

# class Cache(ABC):
#     @abstractmethod
#     async def __init__(self, host: str, port: int, password: str, db: int) -> None:
#         pass

#     @abstractmethod
#     async def get(self, key):
#         pass

#     @abstractmethod
#     async def set(self, key, value):
#         pass

#     @abstractmethod
#     async def delete(self, key):
#         pass

#     @abstractmethod
#     async def close(self):
#         pass

#     @abstractmethod
#     async def __aenter__(self):
#         pass

#     @abstractmethod
#     async def __aexit__(self):
#         pass

# class RedisCache:
#     def __init__(
#             self, 
#             host: str, 
#             port: int, 
#             password: str, 
#             db: int,
#     ):
#         self.storage = aioredis.Redis(host=host, port=port, password=password, db=db)

#     async def get(self, key):
#         return await self.storage.get(key)

#     async def set(self, key, value):
#         return await self.storage.set(key, value)
    
#     async def delete(self, key):
#         return await self.storage.delete(key)
    
#     async def close(self):
#         return await self.storage.close()
    
#     async def __aenter__(self):
#         return await self.storage.initialize()

#     async def __aexit__(self):
#         await self.storage.close()