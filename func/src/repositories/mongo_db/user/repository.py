# Jormungandr - Onboarding
from ..base_repository.base import MongoDbBaseRepository

# Third party
from etria_logger import Gladsheim
from decouple import config


class UserRepository(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def find_one_by_cpf(cls, cpf: str) -> dict:
        collection = await cls._get_collection()
        try:
            user = await collection.find_one({"identifier_document.cpf": cpf})
            return user
        except Exception as ex:
            message = f'UserRepository::find_one_by_email::with this query::"cpf":{cpf}'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def update_one_with_suitability_data(cls, user: dict, suitability):
        collection = await cls._get_collection()
        try:
            user_updated = await collection.update_one(user, {"$set": suitability})
            return user_updated
        except Exception as ex:
            message = f'UserRepository::update_one_with_suitability_data::error on update user":{user}'
            Gladsheim.error(error=ex, message=message)
            raise ex
