from abc import abstractmethod, ABC
from contextlib import contextmanager

from motor.core import Collection
from etria_logger import Gladsheim
from motor.motor_asyncio import AsyncIOMotorClient

from ....infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class MongoDbBaseRepository(ABC):
    infra = MongoDBInfrastructure

    @staticmethod
    @abstractmethod
    def _set_collection(mongo_client: AsyncIOMotorClient) -> Collection:
        pass

    @classmethod
    @contextmanager
    def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            collection = cls._set_collection(mongo_client)
            yield collection
        except Exception as error:
            message = 'MongoDbBaseRepository::collection::error on operating collection'
            Gladsheim.error(error=error, message=message)
            raise error
        finally:
            del collection

    @classmethod
    async def find_one(cls, query: dict) -> dict:
        with cls._get_collection() as collection:
            mongo_object = await collection.find_one(query)
            return mongo_object
