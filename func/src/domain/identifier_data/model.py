from ..validators.user_identifier_data import UserIdentifier


class UserIdentifierDataModel:
    def __init__(self, identifier_data_validated: UserIdentifier, unique_id: str):
        self.unique_id = unique_id
        self.cpf = identifier_data_validated.user_identifier.cpf
        self.phone = identifier_data_validated.user_identifier.phone

    async def get_audit_template(self) -> dict:
        user_identifier_template = {
            "cpf": self.cpf,
            "cel_phone": self.phone,
            "unique_id": self.unique_id,
        }
        return user_identifier_template

    async def get_user_identifier_template(self):
        user_identifier_template = {
            "phone": self.phone,
            "unique_id": self.unique_id,
            "identifier_document": {"cpf": self.cpf},
        }
        return user_identifier_template
