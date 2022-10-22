from decouple import config
from motor.core import Collection
from motor.motor_asyncio import AsyncIOMotorClient

from ..base_repository.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):

    @staticmethod
    def _set_collection(mongo_client: AsyncIOMotorClient) -> Collection:
        database = mongo_client[config("MONGODB_DATABASE_NAME")]
        collection = database[config("MONGODB_USER_COLLECTION")]
        return collection

    @classmethod
    async def find_one_by_cpf(cls, cpf: str) -> dict:
        identifier_data_document = await cls.find_one(
            {"identifier_document.cpf": cpf}
        )
        return identifier_data_document

    @classmethod
    async def find_one_by_unique_id(cls, unique_id: str) -> dict:
        user = await cls.find_one({"unique_id": unique_id})
        return user

    @classmethod
    async def update_one_with_user_identifier_data(
        cls, unique_id: str, user_identifier_template: dict
    ):
        with cls._get_collection() as collection:
            user_updated = await collection.update_one(
                {"unique_id": unique_id}, {"$set": user_identifier_template}
            )
            return user_updated
