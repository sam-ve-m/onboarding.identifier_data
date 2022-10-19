# Jormungandr - Onboarding
from datetime import datetime

from ..domain.enums.types import UserOnboardingStep
from ..domain.exceptions.exceptions import (
    CpfAlreadyExists,
    UserUniqueIdNotExists,
    ErrorOnUpdateUser,
    InvalidOnboardingCurrentStep, CpfBlocked,
)
from ..domain.identifier_data.model import UserIdentifierDataModel
from ..domain.validators.user_identifier_data import UserIdentifier
from ..repositories.mongo_db.blocklist.repository import BlockListRepository
from ..repositories.mongo_db.user.repository import UserRepository
from ..transports.audit.transport import Audit
from ..transports.caf.transport import BureauApiTransport
from ..transports.onboarding_steps.transport import OnboardingSteps


class ServiceUserIdentifierData:
    def __init__(self, identifier_data_validated: UserIdentifier, unique_id: str):
        self.user_identifier = UserIdentifierDataModel(
            identifier_data_validated=identifier_data_validated, unique_id=unique_id
        )

    @staticmethod
    async def validate_current_onboarding_step(jwt: str):
        user_current_step = await OnboardingSteps.get_user_current_step(jwt=jwt)
        if not user_current_step == UserOnboardingStep.IDENTIFIER_DATA:
            raise InvalidOnboardingCurrentStep()

    async def register_identifier_data(self) -> bool:
        await Audit.record_message_log(self.user_identifier)
        user_identifier_template = (
            await self.user_identifier.get_user_identifier_template()
        )
        user_updated = await UserRepository.update_one_with_user_identifier_data(
            unique_id=self.user_identifier.unique_id,
            user_identifier_template=user_identifier_template,
        )
        if not user_updated.matched_count:
            raise ErrorOnUpdateUser()
        await BureauApiTransport.create_transaction(self.user_identifier)
        return True

    async def verify_cpf_and_unique_id_exists(self):
        result = await UserRepository.find_one_by_cpf(cpf=self.user_identifier.cpf)
        if result:
            raise CpfAlreadyExists()
        user = await UserRepository.find_one_by_unique_id(
            unique_id=self.user_identifier.unique_id
        )
        if not user:
            raise UserUniqueIdNotExists()

    async def verify_cpf_is_in_blocklist(self):
        is_defaulter = await BlockListRepository.is_cpf_in_block_list(
            verification_data=datetime.utcnow(),
            cpf=self.user_identifier.cpf,
        )
        if is_defaulter:
            raise CpfBlocked()
