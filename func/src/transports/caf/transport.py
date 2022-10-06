from iara_client import Iara, IaraTopics

from src.domain.exceptions.exceptions import ErrorSendingToIaraValidateCPF
from src.domain.identifier_data.model import UserIdentifierDataModel


class BureauApiTransport:
    @staticmethod
    async def create_transaction(user: UserIdentifierDataModel):
        success, reason = await Iara.send_to_iara(
            topic=IaraTopics.CAF_CPF_VALIDATION,
            message={"unique_id": user.unique_id, "cpf": user.cpf},
        )
        if not success:
            raise ErrorSendingToIaraValidateCPF(str(reason))
