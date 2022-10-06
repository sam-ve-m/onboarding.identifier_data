from decouple import config
from ..base_repository.base import MongoDbBaseRepository
from etria_logger import Gladsheim


class BlockListRepository(MongoDbBaseRepository):

    @staticmethod
    def __set_collection(mongo_client):
        database = mongo_client[config("MONGODB_POSEIDON_DATABASE_NAME")]
        collection = database[config("MONGODB_BLOCKLIST_COLLECTION")]
        return collection

    @classmethod
    async def is_cpf_in_block_list(cls, cpf: str, verification_data: float) -> bool:
        identifier_data_document = await cls.find_one({
            "cpf": int(cpf),
            "trading_date": {"$gt": verification_data},
            "release_date": {"$lt": verification_data},
        })
        if identifier_data_document:
            name = identifier_data_document.get("name")
            reason = identifier_data_document.get("reason")
            details = identifier_data_document.get("description_reason")
            Gladsheim.warning(
                f"User with cpf {cpf}, named {name}, blocked because {reason}, {details}."
            )
            return True
        return False
