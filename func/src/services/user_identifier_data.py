# Jormungandr - Onboarding
from ..domain.exceptions import CpfAlreadyExists, UserUniqueIdNotExists, ErrorOnUpdateUser
from ..domain.identifier_data.model import UserIdentifierDataModel
from ..repositories.mongo_db.user.repository import UserRepository
from ..transports.audit.transport import Audit


class ServiceUserIdentifierData:

    def __init__(self, identifier_data_validated: dict, unique_id: str):
        self.user_identifier = UserIdentifierDataModel(
            identifier_data_validated=identifier_data_validated,
            unique_id=unique_id
        )

    async def register_identifier_data(self):
        await Audit.register_user_log(self.user_identifier)
        user_updated = await UserRepository.update_one_with_user_identifier_data(
            unique_id=self.user_identifier.unique_id,
            user_identifier_data=self.user_identifier.get_user_identifier_template()
        )
        if not user_updated.acknowledged:
            raise ErrorOnUpdateUser
        return True

    async def verify_cpf_and_unique_id_exists(self):
        result = await UserRepository.find_one_by_cpf(cpf=self.user_identifier.cpf)
        if result:
            raise CpfAlreadyExists
        user = await UserRepository.find_one_by_unique_id(unique_id=self.user_identifier.unique_id)
        if not user:
            raise UserUniqueIdNotExists

    async def step_validator(self):
        #TODO Chamar fission quando estiver pronta
        """await UserService.onboarding_br_step_validator(
            payload=payload, onboard_step=["user_identifier_data_step"]
        )"""
        pass
