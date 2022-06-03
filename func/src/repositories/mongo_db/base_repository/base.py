# Jormungandr - Onboarding
from ....infrastructures.mongo_db.infrastructure import MongoDBInfrastructure

# Third party
from etria_logger import Gladsheim


class MongoDbBaseRepository:
    infra = MongoDBInfrastructure
    database = None
    collection = None

    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = f'UserRepository::_get_collection::Error when trying to get collection'
            Gladsheim.error(error=ex, message=message)
            raise ex
