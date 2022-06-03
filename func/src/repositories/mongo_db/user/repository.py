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
            identifier_data_document = await collection.find_one({"identifier_document.cpf": cpf})
            return identifier_data_document
        except Exception as ex:
            message = f'UserRepository::find_one_by_email::with this query::"cpf":{cpf}'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def find_one_user(cls, unique_id: str) -> dict:
        collection = await cls._get_collection()
        try:
            user = await collection.find_one({"unique_id": unique_id})
            return user
        except Exception as ex:
            message = f'UserRepository::find_one_user::with this query::"unique_id":{unique_id}'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def update_one_with_user_identifier_data(cls, unique_id: dict, user_identifier_data):
        collection = await cls._get_collection()
        try:
            user_updated = await collection.update_one({"unique_id": unique_id}, {"$set": user_identifier_data})
            return user_updated
        except Exception as ex:
            message = f'UserRepository::update_one_with_user_identifier_data::error on update identifier data":{user_identifier_data}'
            Gladsheim.error(error=ex, message=message)
            raise ex
