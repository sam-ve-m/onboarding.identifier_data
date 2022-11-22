from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

from ...domain.enums.types import QueueTypes
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.identifier_data.model import UserIdentifierDataModel


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, user_model: UserIdentifierDataModel) -> bool:
        partition = QueueTypes.USER_IDENTIFIER_DATA
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_USER_IDENTIFIER_SCHEMA")
        message = await user_model.get_audit_template()
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            Gladsheim.error(
                message="Audit::register_user_log::Error on trying to register log"
            )
            raise ErrorOnSendAuditLog
        return True
