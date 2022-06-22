class UserIdentifierDataModel:
    def __init__(self, identifier_data_validated, unique_id):
        self.unique_id = unique_id
        self.cpf = identifier_data_validated["user_identifier"].get("cpf")
        self.phone = identifier_data_validated["user_identifier"].get("phone")

    def get_audit_template(self) -> dict:
        user_identifier_template = {
            "cpf": self.cpf,
            "cel_phone": self.phone,
            "unique_id": self.unique_id,
        }
        return user_identifier_template

    def get_user_identifier_template(self):
        user_identifier_template = {
            "phone": self.phone,
            "unique_id": self.unique_id,
            "identifier_document": {"cpf": self.cpf}
        }
        return user_identifier_template
