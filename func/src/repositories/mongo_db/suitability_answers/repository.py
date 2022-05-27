from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from ..base_repository.base import MongoDbBaseRepository

from etria_logger import Gladsheim
from decouple import config


class SuitabilityRepository(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_SUITABILITY_ANSWERS_COLLECTION")

    @classmethod
    async def find_most_recent_suitability_answers(cls) -> list:
        sort = ("_id", -1)
        limit = 1
        try:
            collection = await cls._get_collection()
            cursor = collection.find()
            cursor.sort(*sort)
            suitability_answers = await cursor.to_list(limit)
            return suitability_answers
        except Exception as ex:
            message = f"SuitabilityRepository::find_last_suitability_answer:: error on trying to get suitability answers"
            Gladsheim.error(error=ex, message=message)
            raise ex
